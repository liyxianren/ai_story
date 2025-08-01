#!/usr/bin/env python3
"""
Email Service for AI Storytelling Platform
Handles password reset email notifications
"""

from flask import Flask, render_template_string
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, app=None):
        self.app = app
        self.mail = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Flask-Mail with app"""
        # Email configuration for Outlook/Hotmail
        app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        
        # These should be set via environment variables or config file
        # For development, you can set them directly here
        app.config['MAIL_USERNAME'] = 'lehan_liang@outlook.com'  # Your actual email
        app.config['MAIL_PASSWORD'] = 'your-outlook-password'     # Replace with your Outlook password
        app.config['MAIL_DEFAULT_SENDER'] = 'AI Storytelling Platform <lehan_liang@outlook.com>'
        
        self.mail = Mail(app)
        self.app = app
        
        logger.info("Email service initialized with Flask-Mail")
    
    def send_password_reset_email(self, user_email, username, reset_token, reset_url):
        """Send password reset email to user"""
        try:
            if not self.mail:
                logger.error("Email service not initialized")
                return False
            
            # Email subject
            subject = "StoryKeeper - Password Reset Request"
            
            # Email body (HTML template)
            html_body = self._get_password_reset_template(username, reset_url)
            
            # Create message
            msg = Message(
                subject=subject,
                recipients=[user_email],
                html=html_body
            )
            
            # Send email
            self.mail.send(msg)
            logger.info(f"Password reset email sent successfully to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user_email}: {str(e)}")
            return False
    
    def _get_password_reset_template(self, username, reset_url):
        """Get HTML template for password reset email"""
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset - StoryKeeper Platform</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                }
                .email-container {
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #f0f0f0;
                }
                .logo {
                    font-size: 24px;
                    font-weight: bold;
                    color: #d97706;
                    margin-bottom: 8px;
                }
                .subtitle {
                    color: #6b7280;
                    font-size: 14px;
                }
                .content {
                    margin-bottom: 30px;
                }
                .greeting {
                    font-size: 18px;
                    margin-bottom: 20px;
                    color: #1f2937;
                }
                .message {
                    margin-bottom: 25px;
                    line-height: 1.7;
                }
                .reset-button {
                    display: inline-block;
                    background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
                    color: white;
                    padding: 14px 30px;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    text-align: center;
                    margin: 20px 0;
                    transition: all 0.3s ease;
                }
                .reset-button:hover {
                    background: linear-gradient(135deg, #b45309 0%, #92400e 100%);
                    transform: translateY(-2px);
                }
                .url-fallback {
                    background: #f3f4f6;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 20px 0;
                    word-break: break-all;
                    font-family: monospace;
                    font-size: 12px;
                    color: #4b5563;
                }
                .warning {
                    background: #fef3cd;
                    border: 1px solid #f59e0b;
                    border-radius: 6px;
                    padding: 15px;
                    margin: 20px 0;
                }
                .warning-icon {
                    color: #f59e0b;
                    margin-right: 8px;
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    color: #6b7280;
                    font-size: 12px;
                }
                .divider {
                    margin: 30px 0;
                    border-top: 1px solid #e5e7eb;
                }
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <div class="logo">📖 StoryKeeper</div>
                    <div class="subtitle">AI Storytelling Platform</div>
                </div>
                
                <div class="content">
                    <div class="greeting">Hello {{ username }},</div>
                    
                    <div class="message">
                        We received your password reset request. If this was initiated by you, please click the button below to reset your password:
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{{ reset_url }}" class="reset-button">
                            🔑 Reset My Password
                        </a>
                    </div>
                    
                    <div class="message">
                        If the above button doesn't work, please copy and paste the following link into your browser:
                    </div>
                    
                    <div class="url-fallback">
                        {{ reset_url }}
                    </div>
                    
                    <div class="warning">
                        <span class="warning-icon">⚠️</span>
                        <strong>Security Reminder:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>This link will expire in <strong>15 minutes</strong></li>
                            <li>如果您没有请求密码重置，请忽略此邮件</li>
                            <li>请勿将此链接分享给任何人</li>
                        </ul>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div class="message" style="color: #6b7280; font-size: 14px;">
                        <strong>English:</strong><br>
                        Hello {{ username }}, we received a password reset request for your account. 
                        If you initiated this request, please click the button above to reset your password. 
                        This link will expire in 15 minutes. If you didn't request this, please ignore this email.
                    </div>
                </div>
                
                <div class="footer">
                    <p>此邮件来自故事传承平台 AI Storytelling Platform</p>
                    <p>如有疑问，请联系我们的技术支持</p>
                    <p style="margin-top: 15px; color: #9ca3af;">
                        请勿回复此邮件 | This is an automated email, please do not reply
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Simple template rendering (replace placeholders)
        html_body = template.replace('{{ username }}', username)
        html_body = html_body.replace('{{ reset_url }}', reset_url)
        
        return html_body

    def send_test_email(self, recipient_email):
        """Send a test email to verify email configuration"""
        try:
            if not self.mail:
                logger.error("Email service not initialized")
                return False
            
            msg = Message(
                subject="故事传承平台 - 邮件服务测试",
                recipients=[recipient_email],
                html="""
                <h2>🎉 邮件服务测试成功！</h2>
                <p>如果您收到这封邮件，说明故事传承平台的邮件服务已经正确配置。</p>
                <p><strong>Email Service Test Successful!</strong></p>
                <p>If you received this email, the AI Storytelling Platform email service is properly configured.</p>
                """
            )
            
            self.mail.send(msg)
            logger.info(f"Test email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test email to {recipient_email}: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()

# Fallback email function using basic SMTP (if Flask-Mail fails)
def send_password_reset_email_fallback(user_email, username, reset_url):
    """Fallback email function using basic SMTP"""
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"  # Replace with actual email
        sender_password = "your-app-password"   # Replace with actual app password
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "故事传承 - 密码重置请求"
        msg['From'] = f"故事传承平台 <{sender_email}>"
        msg['To'] = user_email
        
        # Simple text version
        text_body = f"""
        你好 {username}，
        
        我们收到了您的密码重置请求。请点击以下链接重置您的密码：
        
        {reset_url}
        
        此链接将在15分钟后过期。如果您没有请求密码重置，请忽略此邮件。
        
        故事传承平台
        """
        
        text_part = MIMEText(text_body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # Connect and send
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logger.info(f"Fallback password reset email sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send fallback email to {user_email}: {str(e)}")
        return False