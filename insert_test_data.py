#!/usr/bin/env python3
"""
Test Data Insertion Script for AI Storytelling Platform
This script inserts sample users, stories, and related data for testing
"""

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

# Database configuration
DB_CONFIG = {
    'host': 'tpe1.clusters.zeabur.com',
    'port': 32149,
    'user': 'root',
    'password': '69uc42U0oG7Js5Cm831ylixRqHODwXLI',
    'database': 'zeabur'
}

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def insert_test_users():
    """Insert test users"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        print("👥 Inserting test users...")
        
        test_users = [
            ('alice_storyteller', 'alice@example.com', 'password123', '13812345678', None, '我是Alice，喜欢写奇幻冒险故事！'),
            ('bob_writer', 'bob@example.com', 'password123', '13887654321', None, 'Bob here! I love creating romantic comedies.'),
            ('charlie_tales', 'charlie@example.com', 'password123', None, None, 'Charlie - Mystery and thriller enthusiast'),
            ('diana_dreams', 'diana@example.com', 'password123', '13900112233', None, '戴安娜，专注于家庭温馨故事创作'),
            ('admin_user', 'admin@storytelling.com', 'admin123', None, None, 'System Administrator')
        ]
        
        for username, email, password, phone, profile_pic, bio in test_users:
            # Hash the password
            password_hash = generate_password_hash(password)
            
            query = """
            INSERT IGNORE INTO users (username, email, password_hash, phone_number, profile_picture, bio)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, password_hash, phone, profile_pic, bio))
        
        connection.commit()
        print("✅ Test users inserted successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error inserting test users: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def insert_test_stories():
    """Insert test stories"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        print("📚 Inserting test stories...")
        
        # Get user IDs
        cursor.execute("SELECT id, username FROM users WHERE username != 'admin_user'")
        users = cursor.fetchall()
        
        test_stories = [
            {
                'title': '魔法森林的秘密',
                'content': '''在一个遥远的魔法森林里，住着一只会说话的小兔子露娜。露娜有着雪白的毛发和闪闪发光的蓝色眼睛。

有一天，露娜发现森林深处出现了奇怪的光芒。好奇心驱使她踏上了探险之旅。沿着发光的小径，她遇到了智慧的猫头鹰先生、调皮的松鼠兄弟，还有神秘的蝴蝶仙子。

经过重重考验，露娜发现那道光芒来自一颗古老的许愿树。树精告诉她，只要心怀善意，任何愿望都能实现。露娜许下了一个美好的愿望——希望森林里的所有动物都能和谐相处，永远快乐。

从那天起，魔法森林变得更加美丽，动物们也更加友爱。而露娜，成为了森林的守护者。''',
                'language': 'zh-CN',
                'language_name': '中文',
                'description': '一个关于魔法森林中小兔子露娜冒险的温馨故事，教导孩子们善良和友爱的重要性。',
                'word_count': 185,
                'reading_time': 1,
                'status': 'published',
                'user_id': users[0][0],  # alice_storyteller
                'tags': [1, 7, 13, 19, 26, 32]  # Adventure, Happy, Family, Children, Short, Fantasy World
            },
            {
                'title': 'The Coffee Shop Romance',
                'content': '''Emma had been coming to "The Daily Grind" coffee shop every morning for two years, always ordering the same thing: a medium cappuccino with an extra shot of espresso. She was a creature of habit, finding comfort in routine.

What she didn't know was that Jake, the barista with the warm smile and paint-stained fingers, had been secretly perfecting her drink each day, trying to create the perfect cup just for her.

One rainy Tuesday morning, Emma's usual table was taken. Jake noticed her looking around nervously and did something he'd never done before – he left his station and approached her.

"Would you like to share my table?" he asked, gesturing to a small corner spot near the window. "I'm on my break, and I noticed you seemed a bit lost without your usual spot."

As they sat together, Emma learned that Jake was an art student who worked mornings to pay for school. Jake discovered that Emma was a freelance writer who came to the coffee shop for inspiration.

Their conversation flowed as naturally as the coffee Jake had been perfecting for her. By the time Emma had to leave for a client meeting, they had planned to meet for dinner that weekend.

Sometimes, the best love stories begin with a perfect cup of coffee and the courage to break routine.''',
                'language': 'en-US',
                'language_name': 'English',
                'description': 'A heartwarming romance that blooms in a cozy coffee shop between a regular customer and a barista.',
                'word_count': 245,
                'reading_time': 2,
                'status': 'published',
                'user_id': users[1][0],  # bob_writer
                'tags': [2, 8, 15, 22, 27, 31]  # Romance, Inspiring, Love, Young Adults, Short, Modern
            },
            {
                'title': 'The Missing Painting',
                'content': '''Detective Sarah Martinez stared at the empty frame hanging on the gallery wall. The priceless Van Gogh painting that had been there just hours ago was now gone, leaving only faint dust marks and a security system that showed no signs of tampering.

"Impossible," muttered the gallery owner, Mr. Whitmore, wringing his hands. "The sensors, the cameras, the motion detectors – everything was working perfectly."

Sarah examined the frame more closely. Something caught her eye – a tiny smudge of blue paint on the corner of the frame, still wet. She looked around the gallery and noticed similar blue smudges on three other frames, all leading in a specific direction.

Following the trail, Sarah found herself in the gallery's restoration room. There, sitting calmly at an easel, was Mrs. Elderwood, the gallery's 78-year-old security guard, carefully cleaning what appeared to be the missing Van Gogh.

"Mrs. Elderwood?" Sarah asked carefully.

The elderly woman looked up with kind eyes. "Oh dear, I suppose you've found me out. You see, I used to be a professional art restorer before I retired. When I saw how dirty this poor painting had become, I just couldn't help myself. I was going to put it back before anyone noticed."

Sarah couldn't help but smile. Sometimes the greatest mysteries have the most innocent solutions.''',
                'language': 'en-US',
                'language_name': 'English',
                'description': 'A clever mystery about a missing painting and an unexpected culprit with good intentions.',
                'word_count': 278,
                'reading_time': 2,
                'status': 'published',
                'user_id': users[2][0],  # charlie_tales
                'tags': [4, 12, 18, 23, 27, 31]  # Mystery, Suspenseful, Life Lessons, Adults, Short, Modern
            },
            {
                'title': '奶奶的围巾',
                'content': '''小雨坐在床边，手里拿着奶奶亲手织的围巾。围巾是淡蓝色的，上面有着复杂而美丽的花纹，每一针每一线都饱含着奶奶的爱意。

奶奶去世已经一年了，但每当小雨戴上这条围巾，就能感受到奶奶温暖的怀抱。围巾上还残留着奶奶身上特有的茉莉花香味。

今天是小雨的生日，也是她第一次没有奶奶陪伴的生日。妈妈为她准备了生日蛋糕，爸爸买了她喜欢的书，但小雨还是觉得少了什么。

傍晚时分，小雨独自坐在花园里，将围巾轻柔地围在脖子上。微风轻抚，围巾的一角飘了起来，就像奶奶在轻抚她的脸颊。

"奶奶，您在天堂还好吗？"小雨轻声问道。

就在这时，一只美丽的蝴蝶飞到了围巾上，停留了很久很久。小雨相信，那是奶奶在告诉她：我一直都在你身边，我的爱永远包围着你。

从那天起，小雨明白了，爱是不会因为离别而消失的，它会以各种方式陪伴我们一生。''',
                'language': 'zh-CN',
                'language_name': '中文',
                'description': '一个关于祖孙情深的感人故事，讲述爱如何超越生死，永远陪伴我们。',
                'word_count': 198,
                'reading_time': 1,
                'status': 'published',
                'user_id': users[3][0],  # diana_dreams
                'tags': [6, 8, 13, 25, 26, 31]  # Drama, Inspiring, Family, Family, Short, Modern
            },
            {
                'title': 'The Midnight Garden',
                'content': '''Every night at exactly midnight, ten-year-old Oliver would sneak out of his bedroom and tiptoe to the window. What he saw there defied all logic – his grandmother's ordinary daytime garden transformed into something magical.

The roses glowed with soft silver light, the fountain sparkled like liquid diamonds, and tiny fairy lights danced between the leaves of the old oak tree. Most amazingly of all, Oliver could see his late grandfather sitting on their favorite bench, reading a book under the moonlight.

One night, Oliver gathered enough courage to climb out of the window and walk into the midnight garden. As his bare feet touched the cool grass, everything felt perfectly real – the sweet scent of night-blooming jasmine, the gentle tinkle of the fountain, even his grandfather's familiar voice.

"I've been waiting for you to visit, young man," his grandfather said with a warm smile, closing his book and patting the bench beside him.

They spent the night talking about everything and nothing – school, dreams, the stars, and the secret that gardens hold different magic in the daylight and in the darkness.

As dawn approached, his grandfather stood up. "Remember, Oliver, magic exists for those who believe in it. But some magic is meant to be kept secret, just between us."

Oliver nodded solemnly, and when he blinked, he was back in his bedroom, wondering if it had all been a dream. But the smell of jasmine on his pajamas told him otherwise.

From then on, Oliver visited the midnight garden whenever he needed comfort, advice, or simply wanted to feel the magic that exists in the space between dreams and reality.''',
                'language': 'en-US',
                'language_name': 'English',
                'description': 'A magical story about a boy who discovers his grandmother\'s garden transforms into something extraordinary at midnight.',
                'word_count': 312,
                'reading_time': 2,
                'status': 'draft',
                'user_id': users[0][0],  # alice_storyteller
                'tags': [3, 7, 13, 19, 28, 32]  # Fantasy, Happy, Family, Children, Medium, Fantasy World
            }
        ]
        
        for story_data in test_stories:
            # Insert story
            story_query = """
            INSERT INTO stories (user_id, title, content, language, language_name, description, 
                               word_count, reading_time, status, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            published_at = datetime.now() - timedelta(days=random.randint(1, 30)) if story_data['status'] == 'published' else None
            
            cursor.execute(story_query, (
                story_data['user_id'], story_data['title'], story_data['content'],
                story_data['language'], story_data['language_name'], story_data['description'],
                story_data['word_count'], story_data['reading_time'], story_data['status'], published_at
            ))
            
            # Get the inserted story ID
            story_id = cursor.lastrowid
            
            # Insert story tags
            for tag_id in story_data['tags']:
                tag_query = "INSERT IGNORE INTO story_tags (story_id, tag_id) VALUES (%s, %s)"
                cursor.execute(tag_query, (story_id, tag_id))
            
            # Add some random views and likes for published stories
            if story_data['status'] == 'published':
                view_count = random.randint(10, 100)
                like_count = random.randint(1, 20)
                
                # Update view and like counts
                cursor.execute("UPDATE stories SET view_count = %s, like_count = %s WHERE id = %s", 
                             (view_count, like_count, story_id))
        
        connection.commit()
        print("✅ Test stories inserted successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error inserting test stories: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def display_test_data():
    """Display inserted test data"""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        print("\n" + "="*60)
        print("📊 TEST DATA SUMMARY")
        print("="*60)
        
        # Users count
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"👥 Users: {user_count}")
        
        # Stories count by status
        cursor.execute("SELECT status, COUNT(*) FROM stories GROUP BY status")
        story_stats = cursor.fetchall()
        print("📚 Stories:")
        for status, count in story_stats:
            print(f"   - {status}: {count}")
        
        # Categories and tags count
        cursor.execute("SELECT COUNT(*) FROM tag_categories")
        category_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tags")
        tag_count = cursor.fetchone()[0]
        print(f"🏷️  Categories: {category_count}")
        print(f"🏷️  Tags: {tag_count}")
        
        # Recent stories
        print("\n📖 Recent Test Stories:")
        cursor.execute("""
            SELECT s.title, u.username, s.status, s.language_name, s.word_count
            FROM stories s 
            JOIN users u ON s.user_id = u.id 
            ORDER BY s.created_at DESC 
            LIMIT 5
        """)
        stories = cursor.fetchall()
        
        for title, username, status, language, word_count in stories:
            print(f"   📝 '{title}' by {username} ({language}, {word_count} words, {status})")
        
        print("\n✅ Test data ready for use!")
        
    except Error as e:
        print(f"❌ Error displaying test data: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    """Main execution function"""
    print("🧪 AI STORYTELLING PLATFORM - TEST DATA INSERTION")
    print("="*55)
    
    # Insert test users
    if not insert_test_users():
        print("❌ Failed to insert test users!")
        return
    
    # Insert test stories
    if not insert_test_stories():
        print("❌ Failed to insert test stories!")
        return
    
    # Display summary
    display_test_data()
    
    print("\n🎉 TEST DATA INSERTION COMPLETED!")
    print("✅ Ready for testing the story publishing system!")

if __name__ == "__main__":
    main()