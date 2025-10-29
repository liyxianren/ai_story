#!/usr/bin/env python3
"""
Audio Upload and Processing Service for AI Storytelling Platform
Handles audio uploads, validation, and storage
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioService:
    """Service for handling audio uploads and processing"""

    def __init__(self, upload_folder: str = '/video/stories'):
        """
        Initialize the audio service

        Args:
            upload_folder (str): Base folder for audio uploads
        """
        self.upload_folder = upload_folder
        self.allowed_extensions = {'webm', 'mp3', 'wav', 'm4a', 'ogg', 'mp4'}
        self.max_file_size = 25 * 1024 * 1024  # 25MB
        self.max_duration = 3600  # 60 minutes in seconds

        # Ensure upload directory exists
        self._ensure_upload_directory()

        logger.info(f"Audio service initialized with upload folder: {upload_folder}")

    def _ensure_upload_directory(self):
        """Ensure the upload directory structure exists"""
        try:
            # Create base upload directory
            os.makedirs(self.upload_folder, exist_ok=True)

            # Create year/month subdirectories for current date
            current_date = datetime.now()
            year_month = current_date.strftime('%Y/%m')
            full_path = os.path.join(self.upload_folder, year_month)
            os.makedirs(full_path, exist_ok=True)

            logger.info(f"Upload directory ensured: {full_path}")

        except Exception as e:
            logger.error(f"Failed to create upload directory: {str(e)}")
            raise

    def is_allowed_file(self, filename: str) -> bool:
        """
        Check if the file extension is allowed

        Args:
            filename (str): The filename to check

        Returns:
            bool: True if allowed, False otherwise
        """
        return ('.' in filename and
                filename.rsplit('.', 1)[1].lower() in self.allowed_extensions)

    def _detect_audio_format(self, audio_data: bytes) -> str:
        """
        Detect audio format from magic bytes

        Args:
            audio_data (bytes): Audio file data

        Returns:
            str: Detected format or 'unknown'
        """
        if audio_data[:4] == b'RIFF':
            return 'wav'
        elif audio_data[:3] == b'ID3' or audio_data[:2] == b'\xff\xfb':
            return 'mp3'
        elif audio_data[:4] == b'ftyp':
            return 'm4a'
        elif audio_data[:4] == b'\x1a\x45\xdf\xa3':
            return 'webm'
        elif audio_data[:4] == b'OggS':
            return 'ogg'
        else:
            return 'unknown'

    def validate_audio_file(self, file: FileStorage) -> Dict[str, Any]:
        """
        Validate the uploaded audio file

        Args:
            file (FileStorage): The uploaded file

        Returns:
            Dict[str, Any]: Validation result with success status and error message
        """
        try:
            # Check if file exists
            if not file or not file.filename:
                return {
                    'success': False,
                    'error': 'No file selected'
                }

            # Check file extension
            if not self.is_allowed_file(file.filename):
                return {
                    'success': False,
                    'error': f'Unsupported file format. Supported formats: {", ".join(self.allowed_extensions)}'
                }

            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset file pointer

            if file_size > self.max_file_size:
                max_size_mb = self.max_file_size / (1024 * 1024)
                return {
                    'success': False,
                    'error': f'File too large. Maximum size supported: {max_size_mb:.1f}MB'
                }

            # Basic validation passed
            return {
                'success': True,
                'file_size': file_size
            }

        except Exception as e:
            logger.error(f"Audio validation error: {str(e)}")
            return {
                'success': False,
                'error': f'File validation failed: {str(e)}'
            }

    def upload_story_audio(self, file: FileStorage, user_id: int, story_id: Optional[int] = None, duration: Optional[int] = None) -> Dict[str, Any]:
        """
        Upload and process a story audio file

        Args:
            file (FileStorage): The uploaded audio file
            user_id (int): User ID who owns the story
            story_id (Optional[int]): Story ID (if None, will generate temp ID)
            duration (Optional[int]): Audio duration in seconds

        Returns:
            Dict[str, Any]: Upload result with file path and metadata
        """
        try:
            # Validate the file first
            validation_result = self.validate_audio_file(file)
            if not validation_result['success']:
                return validation_result

            # Generate unique filename
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_id = str(uuid.uuid4())
            story_identifier = f"story_{story_id}" if story_id else f"temp_{unique_id}"

            # Create directory structure: year/month/user_id/
            current_date = datetime.now()
            year_month = current_date.strftime('%Y/%m')
            user_folder = os.path.join(self.upload_folder, year_month, f"user_{user_id}")
            os.makedirs(user_folder, exist_ok=True)

            # Generate filename
            filename = f"{story_identifier}_original.{file_extension}"
            file_path = os.path.join(user_folder, filename)

            # Save the audio file
            file.save(file_path)

            # Store relative path for database
            relative_path = os.path.join(year_month, f"user_{user_id}", filename).replace('\\', '/')

            logger.info(f"Saved audio file: {file_path}")

            # Get audio metadata
            metadata = {
                'original_filename': secure_filename(file.filename),
                'file_size': validation_result['file_size'],
                'upload_date': current_date.isoformat()
            }

            return {
                'success': True,
                'audio_path': relative_path,
                'metadata': metadata,
                'duration': duration,
                'format': file_extension
            }

        except Exception as e:
            logger.error(f"Audio upload error: {str(e)}")
            return {
                'success': False,
                'error': f'Audio upload failed: {str(e)}'
            }

    def delete_story_audio(self, audio_path: str) -> bool:
        """
        Delete story audio from filesystem

        Args:
            audio_path (str): Relative path to the audio file

        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            if audio_path:
                full_path = os.path.join(self.upload_folder, audio_path)
                try:
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        logger.info(f"Deleted audio: {full_path}")
                        return True
                    else:
                        logger.warning(f"Audio not found for deletion: {full_path}")
                        return False
                except Exception as e:
                    logger.error(f"Failed to delete audio {full_path}: {str(e)}")
                    return False

            return True

        except Exception as e:
            logger.error(f"Error deleting story audio: {str(e)}")
            return False

    def get_audio_url(self, relative_path: str) -> str:
        """
        Get the full URL for an audio file

        Args:
            relative_path (str): Relative path to the audio

        Returns:
            str: Full audio URL
        """
        if not relative_path:
            return ''

        return f'/video/stories/{relative_path}'

# Global instance
audio_service = AudioService()
