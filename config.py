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
    MAX_CONTENT_LENGTH = 105 * 1024 * 1024  # 105MB (支持100MB视频上传)
    
    # Environment
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Audio Configuration (for transcription)
    MAX_AUDIO_DURATION = 600  # 10 minutes max
    SUPPORTED_AUDIO_FORMATS = ['webm', 'mp4', 'wav', 'mp3']

    # Audio Upload Configuration (for storage)
    AUDIO_UPLOAD_FOLDER = '/video/stories'
    MAX_AUDIO_SIZE = 30 * 1024 * 1024  # 30MB
    ALLOWED_AUDIO_FORMATS = ['webm', 'mp3', 'wav', 'm4a', 'ogg', 'mp4']
    MAX_AUDIO_STORAGE_DURATION = 3600  # 60 minutes

    # Audio Chunking Configuration
    # 注意：音频通过REST API发送时会被Base64编码，导致体积增大约33%
    # 因此7MB的音频经Base64编码后约为9.3MB，低于Google API的10MB限制
    MAX_CHUNK_SIZE = 7 * 1024 * 1024  # 7MB per chunk (考虑Base64编码膨胀约33%)
    MAX_CHUNK_DURATION = 59  # 59秒（留1秒余量给Google API的60秒限制）

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