from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

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
        connection = mysql.connector.connect(**DB_CONFIG)
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
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    
    return None

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(**DB_CONFIG)

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
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                flash('Username or email already exists!', 'error')
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
            
        except Error as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('register.html')
        finally:
            if 'connection' in locals() and connection.is_connected():
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
                
        except Error as e:
            flash(f'Login failed: {str(e)}', 'error')
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Storytelling dashboard - main hub for voice preservation"""
    return render_template('storytelling_dashboard.html', user=current_user)

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
            
        except Error as e:
            flash(f'Profile update failed: {str(e)}', 'error')
        finally:
            if 'connection' in locals() and connection.is_connected():
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
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

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