import os
import io
import tempfile
from typing import Optional, Dict, Any
import logging
import requests
import base64
import json

from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechTranscriptionService:
    """Service for handling Google Speech-to-Text transcription"""
    
    def __init__(self):
        """Initialize the speech service with API key authentication"""
        self.api_key = Config.GOOGLE_API_KEY
        self.language_mapping = Config.LANGUAGE_MAPPING
        
    def transcribe_audio_rest_api(self, audio_data: bytes, language_code: str = 'en-US') -> Dict[str, Any]:
        """Transcribe audio using Google Speech-to-Text REST API"""
        try:
            # Convert audio to base64 for REST API
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Map frontend language code to Google's format
            google_language_code = self.language_mapping.get(language_code, language_code)
            
            # Prepare request payload
            # Use WEBM_OPUS encoding for WebM files, which is what browsers typically produce
            request_payload = {
                "config": {
                    "encoding": "WEBM_OPUS",
                    "languageCode": google_language_code,
                    "enableAutomaticPunctuation": True,
                    "enableWordTimeOffsets": False,
                    "maxAlternatives": 1,
                    "model": "latest_long"  # Use latest_long model for better accuracy
                },
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
            
            # Parse the response
            if 'results' in result and len(result['results']) > 0:
                transcript = result['results'][0]['alternatives'][0]['transcript']
                confidence = result['results'][0]['alternatives'][0].get('confidence', 0.0)
                
                logger.info(f"Transcription successful: {transcript[:50]}...")
                return {
                    'success': True,
                    'transcript': transcript,
                    'confidence': confidence,
                    'language': google_language_code
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
                return {
                    'success': False,
                    'error': 'Audio file is too large. Please record a shorter audio clip (max 10MB).',
                    'transcript': '',
                    'confidence': 0.0
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

# Global instance
speech_service = SpeechTranscriptionService() 