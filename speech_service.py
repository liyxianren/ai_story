import os
import io
import tempfile
from typing import Optional, Dict, Any
import logging
import requests
import base64
import json

from config import Config
from gemini_service import gemini_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechTranscriptionService:
    """Service for handling Google Speech-to-Text transcription"""
    
    def __init__(self):
        """Initialize the speech service with API key authentication"""
        self.api_key = Config.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not found")
        self.language_mapping = Config.LANGUAGE_MAPPING
        
    def transcribe_audio_rest_api(self, audio_data: bytes, language_code: str = 'en-US') -> Dict[str, Any]:
        """Transcribe audio using Google Speech-to-Text REST API"""
        try:
            # Convert audio to base64 for REST API
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Map frontend language code to Google's format
            google_language_code = self.language_mapping.get(language_code, language_code)
            
            # Detect audio format based on magic bytes
            encoding = self._detect_audio_encoding(audio_data)
            logger.info(f"Detected audio encoding: {encoding}")
            
            # Prepare configuration based on detected encoding
            config = {
                "encoding": encoding,
                "languageCode": google_language_code,
                "enableAutomaticPunctuation": True,
                "enableWordTimeOffsets": False,
                "maxAlternatives": 1,
                "model": "latest_long"  # Use latest_long model for better accuracy
            }
            
            # Add sample rate for WAV files (required for LINEAR16)
            if encoding == "LINEAR16":
                config["sampleRateHertz"] = self._get_wav_sample_rate(audio_data)
                logger.info(f"WAV sample rate: {config['sampleRateHertz']}")
            
            # Prepare request payload
            request_payload = {
                "config": config,
                "audio": {
                    "content": audio_base64
                }
            }
            
            # Make request to Google Speech-to-Text API
            url = f"https://speech.googleapis.com/v1/speech:recognize?key={self.api_key}"
            headers = {
                "Content-Type": "application/json"
            }
            
            logger.info(f"Sending transcription request for language: {google_language_code}")
            response = requests.post(url, headers=headers, data=json.dumps(request_payload))
            
            if response.status_code != 200:
                logger.error(f"Google API error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"Google Speech API error: {response.status_code} - {response.text}",
                    'transcript': '',
                    'confidence': 0.0
                }
            
            result = response.json()
            logger.info(f"Google API response: {result}")
            
            # Parse the response - combine all results
            if 'results' in result and len(result['results']) > 0:
                all_transcripts = []
                all_confidences = []
                
                logger.info(f"Found {len(result['results'])} result segments")
                
                # Extract transcript and confidence from each result
                for i, res in enumerate(result['results']):
                    if 'alternatives' in res and len(res['alternatives']) > 0:
                        segment_transcript = res['alternatives'][0]['transcript']
                        segment_confidence = res['alternatives'][0].get('confidence', 0.0)
                        
                        all_transcripts.append(segment_transcript)
                        all_confidences.append(segment_confidence)
                        
                        logger.info(f"Segment {i+1}: '{segment_transcript[:50]}...' (confidence: {segment_confidence:.3f})")
                
                # Combine all transcripts
                combined_transcript = ' '.join(all_transcripts).strip()
                
                # Calculate average confidence
                average_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
                
                logger.info(f"Combined transcription successful: {combined_transcript[:50]}... (avg confidence: {average_confidence:.3f})")
                
                # Process transcription with Gemini AI for story polishing
                logger.info("Polishing story with Gemini AI...")
                try:
                    gemini_result = gemini_service.process_transcription(combined_transcript, google_language_code)
                    
                    if gemini_result['success']:
                        # Use polished story as the primary transcript
                        polished_story = gemini_result['content']
                        logger.info(f"Story polishing successful: {polished_story[:50]}...")
                        
                        # Validation: Ensure raw and polished are different
                        if polished_story == combined_transcript:
                            logger.warning("Warning: Polished story is identical to raw transcript")
                        
                        return {
                            'success': True,
                            'transcript': polished_story,  # Polished version as main transcript
                            'raw_transcript': combined_transcript,  # Keep original for reference
                            'confidence': average_confidence,
                            'language': 'en-US',  # Final story is always in English
                            'original_language': google_language_code,  # Keep track of original language
                            'segments': len(result['results']),
                            'polished': True,
                            'gemini': gemini_result
                        }
                    else:
                        # Fallback to raw transcript if polishing fails
                        logger.warning(f"Story polishing failed: {gemini_result.get('error', 'Unknown error')}")
                        return {
                            'success': True,
                            'transcript': combined_transcript,  # Raw transcript as fallback
                            'raw_transcript': combined_transcript,
                            'confidence': average_confidence,
                            'language': google_language_code,
                            'segments': len(result['results']),
                            'polished': False,
                            'gemini': gemini_result
                        }
                        
                except Exception as e:
                    logger.error(f"Gemini processing failed, using raw transcription: {str(e)}")
                    return {
                        'success': True,
                        'transcript': combined_transcript,  # Raw transcript as fallback
                        'raw_transcript': combined_transcript,
                        'confidence': average_confidence,
                        'language': google_language_code,
                        'segments': len(result['results']),
                        'polished': False,
                        'gemini': {
                            'success': False,
                            'error': f"Story polishing unavailable: {str(e)}",
                            'content': '',
                            'model': 'gemini-2.5-flash'
                        }
                    }
            else:
                logger.warning("No transcription results found in API response")
                return {
                    'success': False,
                    'error': 'No speech detected in the audio. Please try speaking more clearly or check your microphone.',
                    'transcript': '',
                    'confidence': 0.0
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during transcription: {str(e)}")
            return {
                'success': False,
                'error': f"Network error: {str(e)}",
                'transcript': '',
                'confidence': 0.0
            }
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return {
                'success': False,
                'error': f"Transcription error: {str(e)}",
                'transcript': '',
                'confidence': 0.0
            }
    
    def transcribe_audio(self, audio_data: bytes, language_code: str = 'en-US', input_format: str = 'webm') -> Dict[str, Any]:
        """Main transcription method"""
        try:
            # Validate audio data
            if not audio_data or len(audio_data) == 0:
                return {
                    'success': False,
                    'error': 'No audio data provided',
                    'transcript': '',
                    'confidence': 0.0
                }
            
            # Check audio size (Google has a limit of ~10MB for synchronous recognition)
            if len(audio_data) > 10 * 1024 * 1024:
                logger.error(f"Audio chunk size {len(audio_data)} bytes exceeds Google API limit")
                return {
                    'success': False,
                    'error': 'Audio chunk is too large for Google API (max 10MB per chunk). The chunking algorithm should have split this into smaller pieces.',
                    'transcript': '',
                    'confidence': 0.0,
                    'error_type': 'chunk_size_exceeded'
                }
            
            logger.info(f"Transcribing {len(audio_data)} bytes of {input_format} audio in language: {language_code}")
            
            # For WebM format, directly use the audio data
            result = self.transcribe_audio_rest_api(audio_data, language_code)
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription service error: {str(e)}")
            return {
                'success': False,
                'error': f"Transcription failed: {str(e)}",
                'transcript': '',
                'confidence': 0.0
            }
    
    def _detect_audio_encoding(self, audio_data: bytes) -> str:
        """Detect audio encoding based on magic bytes"""
        try:
            # Check for WAV file signature (RIFF...WAVE)
            if len(audio_data) >= 12:
                if audio_data[:4] == b'RIFF' and audio_data[8:12] == b'WAVE':
                    logger.info("Detected WAV file format")
                    return "LINEAR16"
            
            # Check for WebM file signature
            if len(audio_data) >= 4:
                if audio_data[:4] == b'\x1a\x45\xdf\xa3':  # EBML header for WebM
                    logger.info("Detected WebM file format")
                    return "WEBM_OPUS"
            
            # Check for OGG file signature
            if len(audio_data) >= 4:
                if audio_data[:4] == b'OggS':
                    logger.info("Detected OGG file format")
                    return "OGG_OPUS"
            
            # Check for MP3 file signature
            if len(audio_data) >= 3:
                if audio_data[:3] == b'ID3' or audio_data[:2] == b'\xff\xfb':
                    logger.info("Detected MP3 file format")
                    return "MP3"
            
            # Default fallback - assume WebM for browser recordings
            logger.warning("Could not detect audio format, defaulting to WEBM_OPUS")
            return "WEBM_OPUS"
            
        except Exception as e:
            logger.error(f"Error detecting audio encoding: {e}")
            return "WEBM_OPUS"
    
    def _get_wav_sample_rate(self, audio_data: bytes) -> int:
        """Extract sample rate from WAV file header"""
        try:
            if len(audio_data) >= 28:
                # WAV sample rate is stored at bytes 24-27 (little-endian)
                sample_rate = int.from_bytes(audio_data[24:28], byteorder='little')
                logger.info(f"Extracted WAV sample rate: {sample_rate}")
                return sample_rate
            else:
                logger.warning("WAV file too short to extract sample rate, using default")
                return 16000  # Default sample rate
        except Exception as e:
            logger.error(f"Error extracting WAV sample rate: {e}")
            return 16000  # Default fallback

# Global instance
speech_service = SpeechTranscriptionService() 