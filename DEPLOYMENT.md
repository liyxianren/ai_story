# AI Storytelling Platform - Deployment Guide

## 🚀 Zeabur Deployment Instructions

### Prerequisites
- Zeabur account
- GitHub repository
- MySQL database (Zeabur MySQL service)
- Google Cloud API keys

### 1. Environment Variables Setup

In Zeabur dashboard, set these environment variables:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here

# Database (Auto-configured by Zeabur MySQL)
DB_HOST=your-mysql-host
DB_PORT=your-mysql-port
DB_USER=your-mysql-user
DB_PASSWORD=your-mysql-password
DB_NAME=your-mysql-database

# API Keys
GOOGLE_API_KEY=your-google-cloud-api-key
GEMINI_API_KEY=your-gemini-api-key

# Server Configuration
PORT=5000
```

### 2. Database Setup

The application will automatically connect to your Zeabur MySQL instance. Ensure the following tables exist:
- `users`
- `stories`
- `story_tags`
- `tags`
- `password_reset_tokens`
- `user_feedback`

### 3. File Structure (Production-Ready)

```
ai-storytelling-platform/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── Procfile             # Zeabur deployment config
├── start.py             # Production startup script
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── email_service.py     # Email functionality
├── gemini_service.py    # AI story enhancement
├── image_service.py     # Image upload/processing
├── speech_service.py    # Voice-to-text conversion
├── static/              # Static assets
│   ├── cover.png       # Default story cover
│   └── uploads/        # User-uploaded images
└── templates/          # HTML templates
    ├── admin/          # Admin panel templates
    └── *.html          # User-facing templates
```

### 4. Security Features

✅ **Implemented:**
- Environment-based configuration
- Secure session cookies in production
- SQL injection protection (parameterized queries)
- Input validation and sanitization
- Secure password hashing (bcrypt)
- Admin authentication & authorization
- File upload security (type/size validation)
- HTTPS-ready (SSL termination at Zeabur)

### 5. Production Optimizations

✅ **Completed:**
- Removed debug print statements
- Configured proper logging levels
- Optimized database queries
- Removed unused files and dependencies
- Production-ready error handling
- Gunicorn WSGI server configuration
- Static file serving optimization

### 6. Deployment Steps

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Production-ready deployment"
   git push origin main
   ```

2. **Create Zeabur Service:**
   - Connect GitHub repository
   - Select "Python" template
   - Configure environment variables
   - Deploy

3. **Set up MySQL:**
   - Add Zeabur MySQL service
   - Configure database connection
   - Run database migrations if needed

### 7. Post-Deployment Checklist

- [ ] Verify database connection
- [ ] Test user registration/login
- [ ] Test story recording and publishing
- [ ] Test admin panel access
- [ ] Verify file uploads work
- [ ] Check email functionality
- [ ] Test Google Speech API integration
- [ ] Test Gemini AI enhancement
- [ ] Verify user feedback system

### 8. Monitoring & Maintenance

- Monitor application logs in Zeabur dashboard
- Set up database backups
- Monitor API usage (Google Cloud Console)
- Regular security updates

### 9. Scaling Considerations

- Configure auto-scaling in Zeabur
- Consider CDN for static assets
- Database connection pooling
- Redis for session storage (future enhancement)

## 🔧 Troubleshooting

### Common Issues:

1. **Database Connection Failed:**
   - Check environment variables
   - Verify MySQL service is running
   - Check network connectivity

2. **API Keys Not Working:**
   - Verify Google Cloud API keys
   - Check API quotas and billing
   - Ensure APIs are enabled

3. **File Upload Issues:**
   - Check disk space
   - Verify upload directory permissions
   - Check file size limits

### Support

For deployment issues, check:
- Zeabur documentation
- Application logs
- Database connection status
- Environment variable configuration