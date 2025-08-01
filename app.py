from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql
import bcrypt
import os
from datetime import datetime
import secrets
from speech_service import speech_service
from gemini_service import gemini_service
from image_service import image_service

app = Flask(__name__)
# Use a fixed secret key for development to maintain sessions across restarts
app.secret_key = 'your-fixed-secret-key-for-development-only'  # Fixed key for development

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.session_protection = 'basic'  # Use basic session protection for better compatibility

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
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
    
    return None

def get_db_connection():
    """Get database connection"""
    return pymysql.connect(**DB_CONFIG)

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
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Transcription failed: {str(e)}'
        }), 500

@app.route('/api/test-gemini', methods=['POST'])
@login_required
def test_gemini():
    """Test Gemini AI with custom text input"""
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
@login_required
def chat_with_gemini():
    """Chat with Gemini for story polishing and improvement"""
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
    
    # Determine language for response
    if language.startswith('zh') or language.startswith('cmn'):
        language_instruction = "请用中文回应。"
        system_prompt = """你是一个专业的故事编辑和写作导师。用户正在和你对话来改进他们的故事。你的任务是：

🎯 **对话目标**：
- 帮助用户改进和润色他们的故事
- 提供具体、可行的建议
- 根据用户的要求进行修改
- 保持鼓励和支持的语调

📝 **当前故事**：
{current_story}

💬 **对话历史**：
{chat_history_text}

👤 **用户最新消息**：
{user_message}

请根据用户的消息提供帮助。如果用户要求修改故事，请提供修改后的版本。如果用户寻求建议，请给出具体的改进建议。保持对话自然友好。

{language_instruction}"""
    else:
        language_instruction = "Please respond in English."
        system_prompt = """You are a professional story editor and writing mentor. The user is chatting with you to improve their story. Your tasks are:

🎯 **Conversation Goals**:
- Help the user improve and polish their story
- Provide specific, actionable suggestions
- Make modifications based on user requests
- Maintain an encouraging and supportive tone

📝 **Current Story**:
{current_story}

💬 **Chat History**:
{chat_history_text}

👤 **User's Latest Message**:
{user_message}

Please provide help based on the user's message. If the user requests story modifications, provide the revised version. If the user seeks advice, give specific improvement suggestions. Keep the conversation natural and friendly.

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
        
        # Determine language from content
        language = 'zh-CN' if any('\u4e00' <= char <= '\u9fff' for char in content) else 'en-US'
        
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
        language_raw = request.form.get('language', 'zh-CN')
        language_name = request.form.get('language_name', '中文')
        status = request.form.get('status', 'draft')
        
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
        
        # Handle image upload (temporarily disabled for testing)
        image_path = None
        image_original_name = None
        
        print("🖼️  Image upload temporarily disabled for debugging")
        
        # TODO: Re-enable image upload after fixing main publish issue
        # if 'cover_image' in request.files:
        #     file = request.files['cover_image']
        #     if file and file.filename:
        #         upload_result = image_service.upload_story_image(file, current_user.id)
        #         if upload_result['success']:
        #             image_path = upload_result['main_image_path']
        #             image_original_name = upload_result['metadata']['original_filename']
        
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