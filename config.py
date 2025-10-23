import os
import secrets

class Config:
    """Base configuration"""
    # Flask Configuration - Use secure secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # Database Configuration
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST', 'tpe1.clusters.zeabur.com'),
        'port': int(os.environ.get('DB_PORT', 32149)),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', '69uc42U0oG7Js5Cm831ylixRqHODwXLI'),
        'database': os.environ.get('DB_NAME', 'zeabur'),
        'charset': 'utf8mb4',
        'autocommit': True
    }
    
    # API Keys
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Upload Configuration
    UPLOAD_FOLDER = '/image'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Environment
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Audio Configuration (for transcription)
    MAX_AUDIO_DURATION = 600  # 10 minutes max
    SUPPORTED_AUDIO_FORMATS = ['webm', 'mp4', 'wav', 'mp3']

    # Audio Upload Configuration (for storage)
    AUDIO_UPLOAD_FOLDER = '/video/stories'
    MAX_AUDIO_SIZE = 25 * 1024 * 1024  # 25MB
    ALLOWED_AUDIO_FORMATS = ['webm', 'mp3', 'wav', 'm4a', 'ogg', 'mp4']
    MAX_AUDIO_STORAGE_DURATION = 3600  # 60 minutes

    # Language Mapping: Frontend codes to Google Speech-to-Text codes
    LANGUAGE_MAPPING = {
        'en-US': 'en-US',
        'es-ES': 'es-ES', 
        'zh-CN': 'cmn-Hans-CN',
        'fr-FR': 'fr-FR',
        'de-DE': 'de-DE',
        'ja-JP': 'ja-JP',
        'ko-KR': 'ko-KR',
        'ar-SA': 'ar-SA',
        'ru-RU': 'ru-RU',
        'pt-BR': 'pt-BR'
    } 