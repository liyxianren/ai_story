from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql
import bcrypt
import os
from datetime import datetime, timedelta
import secrets
from functools import wraps
import time
from speech_service import speech_service
from gemini_service import gemini_service
from image_service import image_service
from email_service import email_service

app = Flask(__name__)
# Use a fixed secret key for development to maintain sessions across restarts
app.secret_key = 'your-fixed-secret-key-for-development-only'  # Fixed key for development

# Add built-in functions to Jinja2 environment
app.jinja_env.globals.update(min=min, max=max)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.session_protection = 'basic'  # Use basic session protection for better compatibility

# Initialize email service
email_service.init_app(app)

# Database configuration
DB_CONFIG = {
    'host': 'tpe1.clusters.zeabur.com',
    'port': 32149,
    'user': 'root',
    'password': '69uc42U0oG7Js5Cm831ylixRqHODwXLI',
    'database': 'zeabur'
}

class User(UserMixin):
    def __init__(self, id, username, email, phone_number=None, profile_picture=None, bio=None):
        self.id = id
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.bio = bio

@login_manager.user_loader
def load_user(user_id):
    """Load user from database for Flask-Login"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, username, email, phone_number, profile_picture, bio 
            FROM users WHERE id = %s
        """, (user_id,))
        
        user_data = cursor.fetchone()
        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                phone_number=user_data[3],
                profile_picture=user_data[4],
                bio=user_data[5]
            )
        
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
    
    return None

def get_db_connection():
    """Get database connection"""
    return pymysql.connect(**DB_CONFIG)

# Admin authentication
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'happystory'

# Rate limiting storage (in production, use Redis or database)
rate_limit_store = {}

def check_rate_limit(key, max_attempts=5, window_minutes=15):
    """Simple rate limiting function"""
    now = time.time()
    window_start = now - (window_minutes * 60)
    
    # Clean old entries
    if key in rate_limit_store:
        rate_limit_store[key] = [attempt for attempt in rate_limit_store[key] if attempt > window_start]
    else:
        rate_limit_store[key] = []
    
    # Check if limit exceeded
    if len(rate_limit_store[key]) >= max_attempts:
        return False, max_attempts - len(rate_limit_store[key])
    
    # Add current attempt
    rate_limit_store[key].append(now)
    return True, max_attempts - len(rate_limit_store[key])

def get_client_ip():
    """Get client IP address"""
    # Check for forwarded IP first
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    elif request.environ.get('HTTP_X_REAL_IP'):
        return request.environ['HTTP_X_REAL_IP']
    else:
        return request.remote_addr

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def verify_admin_credentials(username, password):
    """Verify admin credentials"""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def _get_user_friendly_error(error_msg):
    """Convert technical Google API errors to user-friendly messages"""
    error_lower = error_msg.lower()
    
    if 'single channel' in error_lower and 'mono' in error_lower:
        return '音频文件必须是单声道（单轨道）格式。请使用录音软件将音频转换为单声道，或重新录制时选择单声道模式。'
    
    elif 'invalid_argument' in error_lower:
        if 'sample rate' in error_lower:
            return '音频采样率不支持。请使用16kHz或48kHz采样率的音频文件。'
        elif 'encoding' in error_lower:
            return '音频格式不支持。请使用WAV、MP3或FLAC格式的音频文件。'
        else:
            return '音频文件格式有问题。请检查文件是否完整，格式是否正确（建议使用WAV格式）。'
    
    elif 'quota_exceeded' in error_lower or 'quota' in error_lower:
        return '语音识别服务暂时超出配额限制，请稍后再试。'
    
    elif 'unauthenticated' in error_lower:
        return '语音识别服务认证失败，请联系管理员。'
    
    elif 'too large' in error_lower or 'size' in error_lower:
        return '音频文件太大。请使用小于25MB的音频文件，或者压缩音频质量。'
    
    elif 'duration' in error_lower:
        return '音频时长超出限制。请使用时长少于60分钟的音频文件。'
    
    elif 'network' in error_lower or 'connection' in error_lower:
        return '网络连接问题，请检查网络连接后重试。'
    
    else:
        return f'语音识别失败：{error_msg}。请检查音频文件质量，或稍后重试。'

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone_number = request.form.get('phone_number')
        bio = request.form.get('bio')
        
        # Validation
        if not username or not email or not password:
            flash('Username, email, and password are required!', 'error')
            return render_template('register.html')
        
        # Email format validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('This username is already taken! Please choose a different username.', 'error')
                return render_template('register.html')
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('This email address is already registered! Please use a different email or try logging in.', 'error')
                return render_template('register.html')
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert new user
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, phone_number, bio)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, password_hash, phone_number, bio))
            
            connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('register.html')
        finally:
            if 'connection' in locals() and connection.open:
                cursor.close()
                connection.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('login.html')
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Get user from database
            cursor.execute("""
                SELECT id, username, email, password_hash, phone_number, profile_picture, bio 
                FROM users WHERE username = %s OR email = %s
            """, (username, username))
            
            user_data = cursor.fetchone()
            
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[3].encode('utf-8')):
                # Create user object and log in
                user = User(
                    id=user_data[0],
                    username=user_data[1],
                    email=user_data[2],
                    phone_number=user_data[4],
                    profile_picture=user_data[5],
                    bio=user_data[6]
                )
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!', 'error')
                
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
        finally:
            if 'connection' in locals() and connection.open:
                cursor.close()
                connection.close()
    
    return render_template('login.html')

@app.route('/my_stories')
@login_required
def my_stories():
    """用户的故事管理页面 - User's story management page"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 获取当前用户的所有故事
        cursor.execute("""
            SELECT 
                s.id,
                s.title,
                s.description,
                s.content,
                s.status,
                s.image_path,
                s.created_at,
                s.updated_at,
                s.view_count,
                s.like_count,
                GROUP_CONCAT(t.name) as categories
            FROM stories s
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.user_id = %s
            GROUP BY s.id, s.title, s.description, s.content, s.status, s.image_path, s.created_at, s.updated_at, s.view_count, s.like_count
            ORDER BY s.created_at DESC
        """, (current_user.id,))
        
        stories = cursor.fetchall()
        
        # 计算统计数据 - 三种状态：待审核、通过审核、未通过审核
        stats = {
            'total': len(stories),
            'published': len([s for s in stories if s['status'] == 'published']),
            'pending': len([s for s in stories if s['status'] == 'pending']),
            'rejected': len([s for s in stories if s['status'] == 'rejected']),
            'total_views': sum(s['view_count'] or 0 for s in stories)
        }
        
        cursor.close()
        connection.close()
        
        return render_template('my_stories.html', 
                             user=current_user, 
                             stories=stories, 
                             stats=stats)
        
    except Exception as e:
        print(f"Error fetching user stories: {e}")
        # 如果出错，返回空数据
        stats = {'total': 0, 'published': 0, 'pending': 0, 'rejected': 0, 'total_views': 0}
        return render_template('my_stories.html', 
                             user=current_user, 
                             stories=[], 
                             stats=stats)

# 保持向后兼容性的dashboard重定向
@app.route('/dashboard')
@login_required
def dashboard():
    """重定向到我的故事页面 - Redirect to my stories page"""
    return redirect(url_for('my_stories'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        bio = request.form.get('bio')
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Update user profile
            cursor.execute("""
                UPDATE users SET phone_number = %s, bio = %s, updated_at = %s 
                WHERE id = %s
            """, (phone_number, bio, datetime.now(), current_user.id))
            
            connection.commit()
            
            # Update current user object
            current_user.phone_number = phone_number
            current_user.bio = bio
            
            flash('Profile updated successfully!', 'success')
            
        except Exception as e:
            flash(f'Profile update failed: {str(e)}', 'error')
        finally:
            if 'connection' in locals() and connection.open:
                cursor.close()
                connection.close()
    
    return render_template('profile.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    try:
        # Rate limiting for password changes
        client_ip = get_client_ip()
        user_key = f"change_password_{current_user.id}_{client_ip}"
        allowed, remaining = check_rate_limit(user_key, max_attempts=5, window_minutes=15)
        
        if not allowed:
            return jsonify({
                'success': False,
                'error': '密码修改次数过多，请15分钟后再试'
            }), 429
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()
        
        # Validate input
        if not current_password:
            return jsonify({
                'success': False,
                'error': 'Current password is required',
                'field': 'current_password'
            }), 400
        
        if not new_password:
            return jsonify({
                'success': False,
                'error': 'New password is required',
                'field': 'new_password'
            }), 400
        
        # Validate new password strength
        if len(new_password) < 8:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 8 characters long',
                'field': 'new_password'
            }), 400
        
        # Check if password contains both letters and numbers
        import re
        if not re.search(r'[a-zA-Z]', new_password) or not re.search(r'\d', new_password):
            return jsonify({
                'success': False,
                'error': 'Password must contain both letters and numbers',
                'field': 'new_password'
            }), 400
        
        # Check if new password is different from current
        if current_password == new_password:
            return jsonify({
                'success': False,
                'error': 'New password must be different from current password',
                'field': 'new_password'
            }), 400
        
        # Get user from database and verify current password
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT password_hash FROM users WHERE id = %s
        """, (current_user.id,))
        
        user_data = cursor.fetchone()
        if not user_data:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Verify current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), user_data[0].encode('utf-8')):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect',
                'field': 'current_password'
            }), 400
        
        # Hash new password
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update password in database
        cursor.execute("""
            UPDATE users SET password_hash = %s, updated_at = %s 
            WHERE id = %s
        """, (new_password_hash, datetime.now(), current_user.id))
        
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password updated successfully'
        })
        
    except Exception as e:
        print(f"Password change error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while updating password'
        }), 500
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page and API"""
    if request.method == 'GET':
        return render_template('forgot_password.html')
    
    # Handle POST request (API)
    try:
        # Rate limiting for forgot password requests
        client_ip = get_client_ip()
        ip_key = f"forgot_password_{client_ip}"
        allowed, remaining = check_rate_limit(ip_key, max_attempts=3, window_minutes=15)
        
        if not allowed:
            return jsonify({
                'success': False,
                'error': '密码重置请求过于频繁，请15分钟后再试'
            }), 429
        # Get email from JSON data or form data
        if request.is_json:
            data = request.get_json()
            email = data.get('email', '').strip() if data else ''
        else:
            email = request.form.get('email', '').strip()
        
        if not email:
            return jsonify({
                'success': False,
                'error': '请输入邮箱地址'
            }), 400
        
        # Validate email format
        import re
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({
                'success': False,
                'error': '请输入有效的邮箱地址'
            }), 400
        
        # Check if user exists
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, username FROM users WHERE email = %s
        """, (email,))
        
        user_data = cursor.fetchone()
        
        # Check if user exists
        if user_data:
            user_id, username = user_data
            
            # Generate simple reset token (no expiry needed for this simple version)
            reset_token = secrets.token_urlsafe(32)
            
            # Save token to database (24 hour expiry for convenience)
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute("""
                INSERT INTO password_reset_tokens (user_id, token, expires_at)
                VALUES (%s, %s, %s)
            """, (user_id, reset_token, expires_at))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Direct redirect to reset password page
            return jsonify({
                'success': True,
                'redirect': f'/reset-password/{reset_token}',
                'message': f'邮箱验证成功！正在跳转到密码重置页面...'
            })
        else:
            cursor.close()
            connection.close()
            
            return jsonify({
                'success': False,
                'error': '该邮箱地址未注册，请检查后重试'
            }), 400
        
    except Exception as e:
        print(f"Forgot password error: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务暂时不可用，请稍后重试'
        }), 500
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

@app.route('/reset-password/<token>')
def reset_password(token):
    """Password reset page with token validation"""
    try:
        # Validate token exists and is not expired
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT prt.id, prt.user_id, prt.expires_at, prt.used, u.username, u.email
            FROM password_reset_tokens prt
            JOIN users u ON prt.user_id = u.id
            WHERE prt.token = %s
        """, (token,))
        
        token_data = cursor.fetchone()
        
        if not token_data:
            flash('重置链接无效或已过期', 'error')
            return redirect(url_for('forgot_password'))
        
        token_id, user_id, expires_at, used, username, email = token_data
        
        # Check if token is expired
        from datetime import datetime
        if datetime.now() > expires_at:
            flash('重置链接已过期，请重新申请', 'error')
            return redirect(url_for('forgot_password'))
        
        # Check if token is already used
        if used:
            flash('此重置链接已被使用', 'error')
            return redirect(url_for('login'))
        
        cursor.close()
        connection.close()
        
        # Token is valid, show reset password form
        return render_template('reset_password.html', token=token, username=username)
        
    except Exception as e:
        print(f"Password reset page error: {str(e)}")
        flash('服务暂时不可用，请稍后重试', 'error')
        return redirect(url_for('forgot_password'))
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

@app.route('/api/reset-password', methods=['POST'])
def reset_password_api():
    """Complete password reset with new password"""
    try:
        # Rate limiting for password reset completion
        client_ip = get_client_ip()
        ip_key = f"reset_password_{client_ip}"
        allowed, remaining = check_rate_limit(ip_key, max_attempts=5, window_minutes=15)
        
        if not allowed:
            return jsonify({
                'success': False,
                'error': '密码重置尝试过于频繁，请15分钟后再试'
            }), 429
        # Get data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400
        
        token = data.get('token', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if not token:
            return jsonify({
                'success': False,
                'error': '缺少重置令牌'
            }), 400
        
        if not new_password:
            return jsonify({
                'success': False,
                'error': '请输入新密码'
            }), 400
        
        # Validate new password strength
        if len(new_password) < 8:
            return jsonify({
                'success': False,
                'error': '密码长度至少为8个字符'
            }), 400
        
        import re
        if not re.search(r'[a-zA-Z]', new_password) or not re.search(r'\d', new_password):
            return jsonify({
                'success': False,
                'error': '密码必须包含字母和数字'
            }), 400
        
        # Validate token and get user info
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT prt.id, prt.user_id, prt.expires_at, prt.used, u.username
            FROM password_reset_tokens prt
            JOIN users u ON prt.user_id = u.id
            WHERE prt.token = %s
        """, (token,))
        
        token_data = cursor.fetchone()
        
        if not token_data:
            return jsonify({
                'success': False,
                'error': '重置链接无效或已过期'
            }), 400
        
        token_id, user_id, expires_at, used, username = token_data
        
        # Check if token is expired
        from datetime import datetime
        if datetime.now() > expires_at:
            return jsonify({
                'success': False,
                'error': '重置链接已过期，请重新申请密码重置'
            }), 400
        
        # Check if token is already used
        if used:
            return jsonify({
                'success': False,
                'error': '此重置链接已被使用'
            }), 400
        
        # Hash new password
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update user password
        cursor.execute("""
            UPDATE users SET password_hash = %s, updated_at = %s 
            WHERE id = %s
        """, (new_password_hash, datetime.now(), user_id))
        
        # Mark token as used
        cursor.execute("""
            UPDATE password_reset_tokens SET used = TRUE, updated_at = %s 
            WHERE id = %s
        """, (datetime.now(), token_id))
        
        # Clean up old tokens for this user (optional but good practice)
        cursor.execute("""
            DELETE FROM password_reset_tokens 
            WHERE user_id = %s AND (expires_at < %s OR used = TRUE) AND id != %s
        """, (user_id, datetime.now(), token_id))
        
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': '密码重置成功！正在跳转到登录页面...'
        })
        
    except Exception as e:
        print(f"Password reset API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': '密码重置失败，请重试'
        }), 500
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

@app.route('/record')
@login_required
def record_story():
    """Voice recording page"""
    return render_template('record_story.html', user=current_user)

@app.route('/api/users')
@login_required
def api_users():
    """API endpoint to get all users (for admin/testing)"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, username, email, phone_number, bio, created_at 
            FROM users ORDER BY created_at DESC
        """)
        
        users = []
        for user_data in cursor.fetchall():
            users.append({
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'phone_number': user_data[3],
                'bio': user_data[4],
                'created_at': user_data[5].isoformat() if user_data[5] else None
            })
        
        return jsonify({'users': users})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

@app.route('/api/transcribe', methods=['POST'])
@login_required
def transcribe_audio():
    """Transcribe uploaded audio using Google Speech-to-Text"""
    try:
        # Check if audio file is present
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No audio file selected'}), 400
        
        # Get language from form data
        language_code = request.form.get('language', 'en-US')
        
        # Get audio format from filename
        file_extension = audio_file.filename.split('.')[-1].lower() if '.' in audio_file.filename else 'webm'
        
        # Read audio data
        audio_data = audio_file.read()
        
        # Validate audio size (limit to 25MB)
        if len(audio_data) > 25 * 1024 * 1024:
            return jsonify({'success': False, 'error': 'Audio file too large (max 25MB)'}), 400
        
        # Transcribe audio using speech service
        result = speech_service.transcribe_audio(
            audio_data=audio_data,
            language_code=language_code,
            input_format=file_extension
        )
        
        if result['success']:
            # TODO: Save transcription to database
            # Return complete result including raw_transcript for proper display
            return jsonify({
                'success': True,
                'transcript': result['transcript'],
                'raw_transcript': result.get('raw_transcript'),  # 原始转录
                'confidence': result['confidence'],
                'language': result['language'],
                'polished': result.get('polished', False),  # 是否经过润色
                'gemini': result.get('gemini', {}),  # Gemini处理结果
                'segments': result.get('segments', 0)  # 音频分段数
            })
        else:
            # Provide user-friendly error messages for common Google API errors
            error_msg = result['error']
            user_friendly_error = _get_user_friendly_error(error_msg)
            
            return jsonify({
                'success': False,
                'error': user_friendly_error,
                'technical_error': error_msg  # Keep technical error for debugging
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Transcription failed: {str(e)}'
        }), 500

@app.route('/api/test-gemini', methods=['POST'])
def test_gemini():
    """Test Gemini AI with custom text input"""
    # Check authentication manually to return JSON error instead of HTML redirect
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'error': 'Authentication required. Please log in to use Gemini polishing.',
            'error_type': 'authentication_required'
        }), 401
    
    try:
        # Get text and language from request
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '').strip()
        language = data.get('language', 'en-US')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        # Import gemini service
        from gemini_service import gemini_service
        
        # Process text with Gemini
        result = gemini_service.process_transcription(text, language)
        
        return jsonify({
            'success': True,
            'input_text': text,
            'language': language,
            'gemini': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Gemini test failed: {str(e)}'
        }), 500

@app.route('/api/chat-with-gemini', methods=['POST'])
def chat_with_gemini():
    """Chat with Gemini for story polishing and improvement"""
    # Check authentication manually to return JSON error instead of HTML redirect
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'error': 'Authentication required. Please log in to use Gemini chat.',
            'error_type': 'authentication_required'
        }), 401
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
        
        user_message = data.get('message', '').strip()
        current_story = data.get('current_story', '').strip()
        chat_history = data.get('chat_history', [])
        language = data.get('language', 'en-US')
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        if not current_story:
            return jsonify({'success': False, 'error': 'No current story provided'}), 400
        
        # Import gemini service
        from gemini_service import gemini_service
        
        # Create conversational prompt for story improvement
        conversation_prompt = _create_chat_prompt(user_message, current_story, chat_history, language)
        
        # Process with Gemini
        result = gemini_service.process_transcription(conversation_prompt, language)
        
        if result['success']:
            return jsonify({
                'success': True,
                'user_message': user_message,
                'gemini_response': result['content'],
                'model': result['model'],
                'language': language,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to get response from Gemini')
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Chat failed: {str(e)}'
        }), 500

def _create_chat_prompt(user_message: str, current_story: str, chat_history: list, language: str) -> str:
    """Create a conversational prompt for story improvement chat"""
    
    # Check if this is just a greeting or casual conversation
    casual_patterns = ['hello', 'hi', 'hey', '你好', '嗨', '问好', 'how are you', '怎么样', '如何']
    is_casual = any(pattern.lower() in user_message.lower() for pattern in casual_patterns)
    
    # Determine language for response
    if language.startswith('zh') or language.startswith('cmn'):
        language_instruction = "请用中文回应。"
        if is_casual:
            system_prompt = """你是一个友好的AI助手和故事编辑。用户刚刚向你打招呼。

👤 **用户消息**：{user_message}

请自然地回应用户的问候，并询问他们是否需要帮助改进故事，或者有其他问题。保持友好和对话的语调。

{language_instruction}"""
        else:
            system_prompt = """你是一个专业的故事编辑和写作导师。用户正在和你对话。根据用户的消息判断他们需要什么：

🎯 **对话模式**：
- 如果用户想改进故事：提供具体建议和修改版本
- 如果用户只是聊天：自然对话，询问是否需要故事帮助
- 如果用户有问题：回答问题并提供帮助
- 如果用户想讨论：参与讨论并适时引导到故事改进

📝 **当前故事**：
{current_story}

💬 **对话历史**：
{chat_history_text}

👤 **用户最新消息**：
{user_message}

根据用户的具体需求回应。不要强制将所有对话都转向故事润色。如果用户只是想聊天或问候，就正常对话。

{language_instruction}"""
    else:
        language_instruction = "Please respond in English."
        if is_casual:
            system_prompt = """You are a friendly AI assistant and story editor. The user just greeted you.

👤 **User Message**: {user_message}

Please respond naturally to their greeting and ask if they need help improving their story or have any other questions. Keep it friendly and conversational.

{language_instruction}"""
        else:
            system_prompt = """You are a professional story editor and writing mentor. The user is chatting with you. Based on their message, determine what they need:

🎯 **Conversation Modes**:
- If user wants story improvement: Provide specific suggestions and revised versions
- If user is just chatting: Have natural conversation, ask if they need story help
- If user has questions: Answer questions and provide assistance
- If user wants discussion: Engage in discussion and guide toward story improvement when appropriate

📝 **Current Story**:
{current_story}

💬 **Chat History**:
{chat_history_text}

👤 **User's Latest Message**:
{user_message}

Respond based on the user's specific needs. Don't force every conversation toward story polishing. If they just want to chat or greet, have a normal conversation.

{language_instruction}"""
    
    # Format chat history
    chat_history_text = ""
    if chat_history:
        for i, chat in enumerate(chat_history[-5:]):  # Only include last 5 exchanges
            role = chat.get('role', 'unknown')
            content = chat.get('content', '')
            chat_history_text += f"{role.title()}: {content}\n"
    else:
        chat_history_text = "No previous conversation."
    
    return system_prompt.format(
        current_story=current_story,
        chat_history_text=chat_history_text,
        user_message=user_message,
        language_instruction=language_instruction
    )

# =====================================================
# Story Publishing Routes and APIs
# =====================================================

@app.route('/publish_story')
@login_required
def publish_story():
    """Story publishing page"""
    return render_template('publish_story.html')

@app.route('/story/<int:story_id>')
def story_detail(story_id):
    """故事详情页面 - Story detail page"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 获取故事详情和作者信息
        cursor.execute("""
            SELECT 
                s.id, s.title, s.content, s.description, s.language_name,
                s.image_path, s.image_original_name, s.reading_time, s.word_count,
                s.status, s.view_count, s.like_count, s.created_at, s.updated_at, s.published_at,
                u.username as author, u.bio as author_bio,
                GROUP_CONCAT(t.name) as categories
            FROM stories s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.id = %s AND s.status = 'published'
            GROUP BY s.id, s.title, s.content, s.description, s.language_name,
                     s.image_path, s.image_original_name, s.reading_time, s.word_count,
                     s.status, s.view_count, s.like_count, s.created_at, s.updated_at, s.published_at,
                     u.username, u.bio
        """, (story_id,))
        
        story = cursor.fetchone()
        
        if not story:
            flash('故事不存在或暂未发布', 'error')
            return redirect(url_for('story_library'))
        
        # 更新浏览次数
        cursor.execute("UPDATE stories SET view_count = view_count + 1 WHERE id = %s", (story_id,))
        connection.commit()
        story['view_count'] = (story['view_count'] or 0) + 1
        
        # 获取相关故事推荐（同标签或同作者）
        cursor.execute("""
            SELECT s.id, s.title, s.image_path, s.view_count, s.like_count
            FROM stories s
            WHERE s.id != %s AND s.status = 'published'
            ORDER BY s.view_count DESC, s.created_at DESC
            LIMIT 3
        """, (story_id,))
        
        related_stories = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('story_detail.html', 
                             story=story, 
                             related_stories=related_stories)
        
    except Exception as e:
        print(f"Error fetching story detail: {e}")
        flash('获取故事详情失败', 'error')
        return redirect(url_for('story_library'))

@app.route('/story_library')
def story_library():
    """Story library page showing all published stories"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get all published stories with user info and tags
        cursor.execute("""
            SELECT 
                s.id,
                s.title,
                s.description,
                s.image_path,
                s.created_at,
                s.view_count,
                s.like_count,
                u.username as author,
                GROUP_CONCAT(t.name) as categories
            FROM stories s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.status = 'published'
            GROUP BY s.id, s.title, s.description, s.image_path, s.created_at, s.view_count, s.like_count, u.username
            ORDER BY s.created_at DESC
        """)
        
        stories = cursor.fetchall()
        
        # Get unique categories for filtering
        cursor.execute("""
            SELECT DISTINCT t.name
            FROM tags t
            JOIN story_tags st ON t.id = st.tag_id
            JOIN stories s ON st.story_id = s.id
            WHERE s.status = 'published'
            ORDER BY t.name
        """)
        
        categories = [row['name'] for row in cursor.fetchall()]
        
        return render_template('story_library.html', stories=stories, categories=categories)
        
    except Exception as e:
        flash(f'Error loading story library: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/api/get_story_types')
@login_required  
def get_story_types():
    """Get simplified story types for story publishing"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get all story types (simplified tags)
        cursor.execute("""
            SELECT id, name, description, usage_count
            FROM tags 
            WHERE category_id = 1
            ORDER BY id
        """)
        
        story_types = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'story_types': story_types
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to load story types: {str(e)}'
        }), 500

@app.route('/api/generate_description', methods=['POST'])
@login_required
def generate_description():
    """Generate story description using Gemini AI"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Story content is required'
            }), 400
        
        # Since all story content is now in English after Gemini processing
        language = 'en-US'
        
        # Generate description using Gemini
        result = gemini_service.generate_story_description(content, language)
        
        if result['success']:
            return jsonify({
                'success': True,
                'description': result['description']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Description generation failed: {str(e)}'
        }), 500

@app.route('/api/publish_story', methods=['POST'])
@login_required
def publish_story_api():
    """Publish a new story"""
    try:
        print("🚀 Publishing story API called")
        
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        description = request.form.get('description', '').strip()
        language_raw = request.form.get('language', 'en-US')
        language_name = request.form.get('language_name', 'English')
        
        # Since all stories are now translated to English by Gemini, 
        # ensure language is always set to English
        if content:  # If there's content, it's been processed by Gemini and is in English
            language_raw = 'en-US'
            language_name = 'English'
        # 新故事默认为待审核状态，需要管理员审核
        status = 'pending'  # 默认状态为待审核
        
        # Now we have expanded the field, keep the full language code
        language = language_raw if language_raw else 'zh-CN'
        
        # Create language group mapping for story browsing
        def get_language_group(lang_code):
            """Map detailed language codes to main language groups"""
            lang_mappings = {
                # Chinese variants
                'cmn-Hans-CN': 'zh',
                'cmn-Hant-TW': 'zh', 
                'zh-CN': 'zh',
                'zh-TW': 'zh',
                'zh-HK': 'zh',
                # English variants
                'en-US': 'en',
                'en-GB': 'en',
                'en-AU': 'en',
                'en-CA': 'en',
                'en-IN': 'en',
                # Spanish variants
                'es-ES': 'es',
                'es-MX': 'es',
                'es-AR': 'es',
                # French variants
                'fr-FR': 'fr',
                'fr-CA': 'fr',
                # German variants
                'de-DE': 'de',
                'de-AT': 'de',
                # Japanese
                'ja-JP': 'ja',
                # Korean
                'ko-KR': 'ko',
                # Arabic variants
                'ar-SA': 'ar',
                'ar-EG': 'ar',
                # Hindi
                'hi-IN': 'hi',
                # Portuguese variants
                'pt-BR': 'pt',
                'pt-PT': 'pt',
                # Russian
                'ru-RU': 'ru',
                # Italian
                'it-IT': 'it',
                # Dutch
                'nl-NL': 'nl',
                # Thai
                'th-TH': 'th',
                # Vietnamese
                'vi-VN': 'vi'
            }
            
            # Return mapped group or extract the main language code
            if lang_code in lang_mappings:
                return lang_mappings[lang_code]
            else:
                # Fallback: extract the first part before '-'
                return lang_code.split('-')[0] if '-' in lang_code else lang_code
        
        language_group = get_language_group(language)
        
        # Get selected story type
        story_type = request.form.get('story_type')
        
        print(f"📝 Form data: title={title}, content_length={len(content) if content else 0}, status={status}, story_type={story_type}")
        print(f"🌐 Language data: language='{language}' (len={len(language)}), language_name='{language_name}' (len={len(language_name)})")
        
        # Validate required fields
        if not title:
            print("❌ No title provided")
            return jsonify({
                'success': False,
                'error': 'Story title is required'
            }), 400
        
        if not content:
            print("❌ No content provided")
            return jsonify({
                'success': False,
                'error': 'Story content is required'
            }), 400
        
        # Calculate word count and reading time
        word_count = len(content.replace(' ', '')) if any('\u4e00' <= char <= '\u9fff' for char in content) else len(content.split())
        reading_time = max(1, word_count // (200 if language.startswith('zh') else 250))
        
        # Handle image upload
        image_path = None
        image_original_name = None
        
        print("🖼️  Processing image upload...")
        
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename:
                print(f"📸 Uploading image: {file.filename}")
                upload_result = image_service.upload_story_image(file, current_user.id)
                if upload_result['success']:
                    image_path = upload_result['main_image_path']
                    image_original_name = upload_result['metadata']['original_filename']
                    print(f"✅ Image uploaded successfully: {image_path}")
                else:
                    print(f"❌ Image upload failed: {upload_result.get('error', 'Unknown error')}")
            else:
                print("📸 No image file provided")
        else:
            print("📸 No cover_image in request files")
        
        # Insert story into database
        print("💾 Connecting to database...")
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Insert story
        print("📚 Inserting story...")
        story_query = """
            INSERT INTO stories (user_id, title, content, language, language_name, description, 
                               image_path, image_original_name, reading_time, word_count, status, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        published_at = datetime.now() if status == 'published' else None
        
        cursor.execute(story_query, (
            current_user.id, title, content, language, language_name, description,
            image_path, image_original_name, reading_time, word_count, status, published_at
        ))
        
        story_id = cursor.lastrowid
        print(f"✅ Story inserted with ID: {story_id}")
        
        # Insert story type (single tag)
        if story_type and story_type.isdigit():
            print(f"🏷️  Adding story type: {story_type}")
            cursor.execute("INSERT INTO story_tags (story_id, tag_id) VALUES (%s, %s)", (story_id, int(story_type)))
            
            # Update tag usage count
            cursor.execute("UPDATE tags SET usage_count = usage_count + 1 WHERE id = %s", (int(story_type),))
            print("✅ Story type added")
        else:
            print(f"⚠️  No valid story type provided: {story_type}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'story_id': story_id,
            'message': 'Story published successfully!'
        })
        
    except Exception as e:
        print(f"❌ Story publication error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Publication failed: {str(e)}'
        }), 500

@app.route('/api/get_user_stories')
@login_required
def get_user_stories():
    """Get current user's stories"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT s.id, s.title, s.description, s.language_name, s.word_count, 
                   s.reading_time, s.status, s.view_count, s.like_count,
                   s.created_at, s.updated_at, s.published_at, s.image_path,
                   GROUP_CONCAT(t.name) as tags
            FROM stories s
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.user_id = %s
            GROUP BY s.id
            ORDER BY s.created_at DESC
        """, (current_user.id,))
        
        stories = cursor.fetchall()
        
        # Process stories data
        for story in stories:
            story['tags'] = story['tags'].split(',') if story['tags'] else []
            story['image_url'] = image_service.get_image_url(story['image_path']) if story['image_path'] else None
            
            # Format dates
            for date_field in ['created_at', 'updated_at', 'published_at']:
                if story[date_field]:
                    story[date_field] = story[date_field].isoformat()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'stories': stories
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to load stories: {str(e)}'
        }), 500

# =====================================================
# Admin Management Routes
# =====================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_admin_credentials(username, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('管理员登录成功！', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('用户名或密码错误！', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@admin_required
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('已安全退出管理后台', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get system statistics
        stats = {}
        
        # Story statistics by status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM stories 
            GROUP BY status
        """)
        status_stats = cursor.fetchall()
        stats['stories'] = {stat['status']: stat['count'] for stat in status_stats}
        
        # Total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        stats['total_users'] = cursor.fetchone()['count']
        
        # Recent pending stories (last 10)
        cursor.execute("""
            SELECT s.id, s.title, s.created_at, u.username as author
            FROM stories s
            JOIN users u ON s.user_id = u.id
            WHERE s.status = 'pending'
            ORDER BY s.created_at DESC
            LIMIT 10
        """)
        recent_pending = cursor.fetchall()
        
        # Top viewed published stories
        cursor.execute("""
            SELECT s.id, s.title, s.view_count, u.username as author
            FROM stories s
            JOIN users u ON s.user_id = u.id
            WHERE s.status = 'published'
            ORDER BY s.view_count DESC
            LIMIT 5
        """)
        top_stories = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('admin/dashboard.html', 
                             stats=stats,
                             recent_pending=recent_pending,
                             top_stories=top_stories)
        
    except Exception as e:
        flash(f'获取统计数据失败: {str(e)}', 'error')
        return render_template('admin/dashboard.html', 
                             stats={'stories': {}},
                             recent_pending=[],
                             top_stories=[])

@app.route('/admin/stories')
@admin_required
def admin_stories():
    """Admin story management page"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get filter parameters
        status = request.args.get('status', 'pending')
        page = int(request.args.get('page', 1))
        per_page = 20
        offset = (page - 1) * per_page
        
        # Get stories with pagination
        cursor.execute("""
            SELECT s.id, s.title, s.description, s.status, s.created_at, s.updated_at,
                   s.view_count, s.like_count, s.word_count,
                   u.username as author, u.email as author_email,
                   GROUP_CONCAT(t.name) as tags
            FROM stories s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.status = %s
            GROUP BY s.id, s.title, s.description, s.status, s.created_at, s.updated_at,
                     s.view_count, s.like_count, s.word_count, u.username, u.email
            ORDER BY s.created_at DESC
            LIMIT %s OFFSET %s
        """, (status, per_page, offset))
        
        stories = cursor.fetchall()
        
        # Get total count for pagination
        cursor.execute("SELECT COUNT(*) as count FROM stories WHERE status = %s", (status,))
        total_count = cursor.fetchone()['count']
        total_pages = (total_count + per_page - 1) // per_page
        
        # Get status counts for tabs
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM stories 
            GROUP BY status
        """)
        status_counts = {stat['status']: stat['count'] for stat in cursor.fetchall()}
        
        cursor.close()
        connection.close()
        
        return render_template('admin/stories.html',
                             stories=stories,
                             current_status=status,
                             status_counts=status_counts,
                             page=page,
                             total_pages=total_pages,
                             total_count=total_count)
        
    except Exception as e:
        flash(f'获取故事列表失败: {str(e)}', 'error')
        return render_template('admin/stories.html',
                             stories=[],
                             current_status='pending',
                             status_counts={},
                             page=1,
                             total_pages=1,
                             total_count=0)

@app.route('/admin/story/<int:story_id>')
@admin_required
def admin_story_detail(story_id):
    """Admin story detail view"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get story details
        cursor.execute("""
            SELECT s.*, u.username as author, u.email as author_email,
                   GROUP_CONCAT(t.name) as tags
            FROM stories s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.id = %s
            GROUP BY s.id, s.title, s.content, s.description, s.status, s.created_at, 
                     s.updated_at, s.published_at, s.view_count, s.like_count, 
                     s.word_count, s.reading_time, s.language, s.language_name,
                     s.image_path, s.image_original_name, u.username, u.email
        """, (story_id,))
        
        story = cursor.fetchone()
        
        if not story:
            flash('故事不存在', 'error')
            return redirect(url_for('admin_stories'))
        
        cursor.close()
        connection.close()
        
        return render_template('admin/story_detail.html', story=story)
        
    except Exception as e:
        flash(f'获取故事详情失败: {str(e)}', 'error')
        return redirect(url_for('admin_stories'))

# Admin API routes
@app.route('/admin/api/approve_story/<int:story_id>', methods=['POST'])
@admin_required
def admin_approve_story(story_id):
    """Approve a story"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Update story status to published
        cursor.execute("""
            UPDATE stories 
            SET status = 'published', published_at = %s, updated_at = %s
            WHERE id = %s AND status = 'pending'
        """, (datetime.now(), datetime.now(), story_id))
        
        if cursor.rowcount > 0:
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': '故事已审核通过'})
        else:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'error': '故事不存在或状态不正确'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'审核失败: {str(e)}'}), 500

@app.route('/admin/api/reject_story/<int:story_id>', methods=['POST'])
@admin_required
def admin_reject_story(story_id):
    """Reject a story"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Update story status to rejected
        cursor.execute("""
            UPDATE stories 
            SET status = 'rejected', updated_at = %s
            WHERE id = %s AND status = 'pending'
        """, (datetime.now(), story_id))
        
        if cursor.rowcount > 0:
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': '故事已被拒绝'})
        else:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'error': '故事不存在或状态不正确'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'拒绝失败: {str(e)}'}), 500

@app.route('/admin/api/batch_action', methods=['POST'])
@admin_required
def admin_batch_action():
    """Perform batch actions on stories"""
    try:
        data = request.get_json()
        action = data.get('action')
        story_ids = data.get('story_ids', [])
        
        if not action or not story_ids:
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if action == 'approve':
            # Batch approve stories
            placeholders = ','.join(['%s'] * len(story_ids))
            cursor.execute(f"""
                UPDATE stories 
                SET status = 'published', published_at = %s, updated_at = %s
                WHERE id IN ({placeholders}) AND status = 'pending'
            """, [datetime.now(), datetime.now()] + story_ids)
            
        elif action == 'reject':
            # Batch reject stories
            placeholders = ','.join(['%s'] * len(story_ids))
            cursor.execute(f"""
                UPDATE stories 
                SET status = 'rejected', updated_at = %s
                WHERE id IN ({placeholders}) AND status = 'pending'
            """, [datetime.now()] + story_ids)
        else:
            return jsonify({'success': False, 'error': '无效的操作'}), 400
        
        affected_rows = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True, 
            'message': f'成功处理了 {affected_rows} 个故事',
            'affected_count': affected_rows
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'批量操作失败: {str(e)}'}), 500

# =====================================================
# Story Like/Unlike Routes
# =====================================================

@app.route('/api/like_story/<int:story_id>', methods=['POST'])
@login_required
def like_story(story_id):
    """Like a story"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if user already liked this story
        cursor.execute("""
            SELECT id FROM story_likes 
            WHERE user_id = %s AND story_id = %s
        """, (current_user.id, story_id))
        
        existing_like = cursor.fetchone()
        
        if existing_like:
            # Unlike: Remove the like
            cursor.execute("""
                DELETE FROM story_likes 
                WHERE user_id = %s AND story_id = %s
            """, (current_user.id, story_id))
            
            # Decrease like count
            cursor.execute("""
                UPDATE stories 
                SET like_count = GREATEST(0, like_count - 1) 
                WHERE id = %s
            """, (story_id,))
            
            action = 'unliked'
        else:
            # Like: Add the like
            cursor.execute("""
                INSERT INTO story_likes (user_id, story_id) 
                VALUES (%s, %s)
            """, (current_user.id, story_id))
            
            # Increase like count
            cursor.execute("""
                UPDATE stories 
                SET like_count = like_count + 1 
                WHERE id = %s
            """, (story_id,))
            
            action = 'liked'
        
        # Get updated like count
        cursor.execute("SELECT like_count FROM stories WHERE id = %s", (story_id,))
        like_count = cursor.fetchone()[0] or 0
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'action': action,
            'like_count': like_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'点赞操作失败: {str(e)}'
        }), 500

@app.route('/api/check_like_status/<int:story_id>')
@login_required
def check_like_status(story_id):
    """Check if current user has liked a story"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id FROM story_likes 
            WHERE user_id = %s AND story_id = %s
        """, (current_user.id, story_id))
        
        liked = cursor.fetchone() is not None
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'liked': liked
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'检查点赞状态失败: {str(e)}'
        }), 500

# =====================================================
# Story Edit Routes
# =====================================================

@app.route('/edit_story/<int:story_id>')
@login_required
def edit_story(story_id):
    """Edit story page - only for story owner"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get story details and verify ownership
        cursor.execute("""
            SELECT s.*, GROUP_CONCAT(t.name) as tags
            FROM stories s
            LEFT JOIN story_tags st ON s.id = st.story_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.id = %s AND s.user_id = %s
            GROUP BY s.id, s.title, s.content, s.description, s.status, 
                     s.image_path, s.created_at, s.updated_at
        """, (story_id, current_user.id))
        
        story = cursor.fetchone()
        
        if not story:
            flash('故事不存在或您无权编辑', 'error')
            return redirect(url_for('my_stories'))
        
        # Get available story types
        cursor.execute("""
            SELECT id, name, description 
            FROM tags 
            WHERE category_id = 1
            ORDER BY name
        """)
        story_types = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('edit_story.html', story=story, story_types=story_types)
        
    except Exception as e:
        flash(f'获取故事信息失败: {str(e)}', 'error')
        return redirect(url_for('my_stories'))

@app.route('/api/update_story/<int:story_id>', methods=['POST'])
@login_required
def update_story(story_id):
    """Update an existing story"""
    try:
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        description = request.form.get('description', '').strip()
        story_type = request.form.get('story_type')
        
        if not title or not content:
            return jsonify({
                'success': False,
                'error': '标题和内容不能为空'
            }), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Verify story ownership
        cursor.execute("""
            SELECT status FROM stories 
            WHERE id = %s AND user_id = %s
        """, (story_id, current_user.id))
        
        story = cursor.fetchone()
        if not story:
            return jsonify({
                'success': False,
                'error': '故事不存在或您无权编辑'
            }), 403
        
        # Calculate word count and reading time
        word_count = len(content.replace(' ', '')) if any('\u4e00' <= char <= '\u9fff' for char in content) else len(content.split())
        reading_time = max(1, word_count // 200)
        
        # Handle image upload if present
        image_path = None
        image_original_name = None
        
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename:
                upload_result = image_service.upload_story_image(file, current_user.id)
                if upload_result['success']:
                    image_path = upload_result['main_image_path']
                    image_original_name = upload_result['metadata']['original_filename']
        
        # Update story - set status to pending if it was published/rejected
        current_status = story[0]
        new_status = 'pending' if current_status in ['published', 'rejected'] else current_status
        
        update_query = """
            UPDATE stories 
            SET title = %s, content = %s, description = %s, word_count = %s, reading_time = %s,
                updated_at = %s, status = %s
        """
        update_params = [title, content, description, word_count, reading_time, datetime.now(), new_status]
        
        # Add image fields if new image uploaded
        if image_path:
            update_query += ", image_path = %s, image_original_name = %s"
            update_params.extend([image_path, image_original_name])
        
        update_query += " WHERE id = %s AND user_id = %s"
        update_params.extend([story_id, current_user.id])
        
        cursor.execute(update_query, update_params)
        
        # Update story tags
        if story_type and story_type.isdigit():
            # Remove existing tags
            cursor.execute("DELETE FROM story_tags WHERE story_id = %s", (story_id,))
            
            # Add new tag
            cursor.execute("INSERT INTO story_tags (story_id, tag_id) VALUES (%s, %s)", 
                          (story_id, int(story_type)))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Determine message based on status change
        if current_status in ['published', 'rejected'] and new_status == 'pending':
            message = '故事已更新并重新提交审核！'
        else:
            message = '故事已成功更新！'
        
        return jsonify({
            'success': True,
            'message': message,
            'status_changed': current_status != new_status,
            'new_status': new_status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'更新失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Create upload folder for profile pictures
    os.makedirs('static/uploads', exist_ok=True)
    
    print("🚀 Starting Flask Application")
    print("=" * 40)
    print("📊 Database: Connected to Zeabur MySQL")
    print("🌐 URL: http://localhost:8080")
    print("📋 Routes available:")
    print("   - / (Home)")
    print("   - /register (User Registration)")
    print("   - /login (User Login)")
    print("   - /dashboard (User Dashboard)")
    print("   - /profile (User Profile)")
    print("   - /logout (Logout)")
    print("   - /api/users (API - All Users)")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=8080) 