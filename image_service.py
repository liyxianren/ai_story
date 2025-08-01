#!/usr/bin/env python3
"""
Image Upload and Processing Service for AI Storytelling Platform
Handles image uploads, validation, resizing, and storage
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageService:
    """Service for handling image uploads and processing"""
    
    def __init__(self, upload_folder: str = 'static/uploads/stories'):
        """
        Initialize the image service
        
        Args:
            upload_folder (str): Base folder for image uploads
        """
        self.upload_folder = upload_folder
        self.allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.image_sizes = {
            'thumbnail': (300, 300),    # For story cards
            'medium': (800, 600),       # For story detail view
            'original': None            # Keep original size (with max limit)
        }
        self.max_original_size = (1920, 1080)  # Max original size
        
        # Ensure upload directory exists
        self._ensure_upload_directory()
        
        logger.info(f"Image service initialized with upload folder: {upload_folder}")
    
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
    
    def validate_image_file(self, file: FileStorage) -> Dict[str, Any]:
        """
        Validate the uploaded image file
        
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
            
            # Try to open and validate as image
            try:
                image = Image.open(file)
                image.verify()  # Verify it's a valid image
                file.seek(0)  # Reset file pointer after verification
                
                # Check image dimensions (minimum size)
                if image.size[0] < 200 or image.size[1] < 200:
                    return {
                        'success': False,
                        'error': 'Image dimensions too small. Minimum size is 200x200 pixels'
                    }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': 'Invalid image file'
                }
            
            return {
                'success': True,
                'file_size': file_size,
                'image_size': image.size
            }
            
        except Exception as e:
            logger.error(f"Image validation error: {str(e)}")
            return {
                'success': False,
                'error': f'File validation failed: {str(e)}'
            }
    
    def upload_story_image(self, file: FileStorage, user_id: int, story_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Upload and process a story cover image
        
        Args:
            file (FileStorage): The uploaded image file
            user_id (int): User ID who owns the story
            story_id (Optional[int]): Story ID (if None, will generate temp ID)
            
        Returns:
            Dict[str, Any]: Upload result with file paths and metadata
        """
        try:
            # Validate the file first
            validation_result = self.validate_image_file(file)
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
            
            # Process and save different sizes
            image_paths = {}
            original_image = Image.open(file)
            
            # Fix image orientation (handle EXIF rotation)
            original_image = ImageOps.exif_transpose(original_image)
            
            # Convert to RGB if necessary (for JPEG compatibility)
            if original_image.mode in ('RGBA', 'P'):
                rgb_image = Image.new('RGB', original_image.size, (255, 255, 255))
                rgb_image.paste(original_image, mask=original_image.split()[-1] if original_image.mode == 'RGBA' else None)
                original_image = rgb_image
            
            for size_name, dimensions in self.image_sizes.items():
                # Generate filename for this size
                filename = f"{story_identifier}_{size_name}.{file_extension}"
                file_path = os.path.join(user_folder, filename)
                
                # Process image
                if size_name == 'original':
                    # For original, just resize if too large
                    processed_image = original_image.copy()
                    if (processed_image.size[0] > self.max_original_size[0] or 
                        processed_image.size[1] > self.max_original_size[1]):
                        processed_image.thumbnail(self.max_original_size, Image.Resampling.LANCZOS)
                else:
                    # For thumbnails and medium, use smart resizing
                    processed_image = self._smart_resize(original_image, dimensions)
                
                # Save the processed image
                quality = 85 if file_extension.lower() == 'jpg' else None
                if quality:
                    processed_image.save(file_path, quality=quality, optimize=True)
                else:
                    processed_image.save(file_path, optimize=True)
                
                # Store relative path for database
                relative_path = os.path.join(year_month, f"user_{user_id}", filename).replace('\\', '/')
                image_paths[size_name] = relative_path
                
                logger.info(f"Saved {size_name} image: {file_path}")
            
            # Get image metadata
            metadata = {
                'original_filename': secure_filename(file.filename),
                'file_size': validation_result['file_size'],
                'image_dimensions': original_image.size,
                'upload_date': current_date.isoformat()
            }
            
            return {
                'success': True,
                'image_paths': image_paths,
                'metadata': metadata,
                'main_image_path': image_paths['medium']  # Use medium as main display
            }
            
        except Exception as e:
            logger.error(f"Image upload error: {str(e)}")
            return {
                'success': False,
                'error': f'Image upload failed: {str(e)}'
            }
    
    def _smart_resize(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """
        Smart resize image maintaining aspect ratio and cropping if necessary
        
        Args:
            image (Image.Image): Source image
            target_size (Tuple[int, int]): Target dimensions (width, height)
            
        Returns:
            Image.Image: Resized image
        """
        # Calculate ratios
        img_ratio = image.size[0] / image.size[1]
        target_ratio = target_size[0] / target_size[1]
        
        if img_ratio > target_ratio:
            # Image is wider than target ratio, crop width
            new_height = image.size[1]
            new_width = int(new_height * target_ratio)
            left = (image.size[0] - new_width) // 2
            image = image.crop((left, 0, left + new_width, new_height))
        elif img_ratio < target_ratio:
            # Image is taller than target ratio, crop height
            new_width = image.size[0]
            new_height = int(new_width / target_ratio)
            top = (image.size[1] - new_height) // 2
            image = image.crop((0, top, new_width, top + new_height))
        
        # Resize to target size
        return image.resize(target_size, Image.Resampling.LANCZOS)
    
    def delete_story_images(self, image_paths: Dict[str, str]) -> bool:
        """
        Delete story images from filesystem
        
        Args:
            image_paths (Dict[str, str]): Dictionary of image paths to delete
            
        Returns:
            bool: True if all deletions successful, False otherwise
        """
        try:
            all_deleted = True
            
            for size_name, relative_path in image_paths.items():
                if relative_path:
                    full_path = os.path.join('static/uploads/stories', relative_path)
                    try:
                        if os.path.exists(full_path):
                            os.remove(full_path)
                            logger.info(f"Deleted image: {full_path}")
                        else:
                            logger.warning(f"Image not found for deletion: {full_path}")
                    except Exception as e:
                        logger.error(f"Failed to delete image {full_path}: {str(e)}")
                        all_deleted = False
            
            return all_deleted
            
        except Exception as e:
            logger.error(f"Error deleting story images: {str(e)}")
            return False
    
    def get_image_url(self, relative_path: str, size: str = 'medium') -> str:
        """
        Get the full URL for an image
        
        Args:
            relative_path (str): Relative path to the image
            size (str): Image size (thumbnail, medium, original)
            
        Returns:
            str: Full image URL
        """
        if not relative_path:
            return '/static/images/default_story_cover.jpg'  # Default placeholder
        
        # Replace size in filename if needed
        if size != 'medium':  # medium is default
            base_path, ext = os.path.splitext(relative_path)
            if '_medium.' in base_path:
                relative_path = base_path.replace('_medium', f'_{size}') + ext
        
        return f'/static/uploads/stories/{relative_path}'

# Global instance
image_service = ImageService()