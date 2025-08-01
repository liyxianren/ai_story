#!/usr/bin/env python3
"""
Simplified Database Setup Script - Creates tables one by one
This ensures all tables are created correctly without SQL parsing issues
"""

import mysql.connector
from mysql.connector import Error

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

def create_all_tables():
    """Create all tables step by step"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        print("🔧 Creating tables step by step...")
        
        # 1. Create users table (if not exists)
        print("📝 Creating users table...")
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20),
            profile_picture VARCHAR(255),
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(users_table)
        print("✅ Users table created")
        
        # 2. Create tag_categories table
        print("📝 Creating tag_categories table...")
        tag_categories_table = """
        CREATE TABLE IF NOT EXISTS tag_categories (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            color VARCHAR(7) DEFAULT '#6c757d',
            icon VARCHAR(50) DEFAULT 'fas fa-tag',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(tag_categories_table)
        print("✅ Tag categories table created")
        
        # 3. Create tags table
        print("📝 Creating tags table...")
        tags_table = """
        CREATE TABLE IF NOT EXISTS tags (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            category_id INT NOT NULL,
            description TEXT,
            usage_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES tag_categories(id) ON DELETE CASCADE,
            UNIQUE KEY unique_tag_per_category (name, category_id)
        )
        """
        cursor.execute(tags_table)
        print("✅ Tags table created")
        
        # 4. Create stories table
        print("📝 Creating stories table...")
        stories_table = """
        CREATE TABLE IF NOT EXISTS stories (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            content LONGTEXT NOT NULL,
            language VARCHAR(10) NOT NULL,
            language_name VARCHAR(50),
            description TEXT,
            image_path VARCHAR(500),
            image_original_name VARCHAR(255),
            reading_time INT,
            word_count INT,
            status ENUM('draft', 'pending', 'published', 'rejected', 'private', 'archived') DEFAULT 'draft',
            view_count INT DEFAULT 0,
            like_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            published_at TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_language (language),
            INDEX idx_status (status),
            INDEX idx_created_at (created_at),
            INDEX idx_published_at (published_at)
        )
        """
        cursor.execute(stories_table)
        print("✅ Stories table created")
        
        # 5. Create story_tags junction table
        print("📝 Creating story_tags table...")
        story_tags_table = """
        CREATE TABLE IF NOT EXISTS story_tags (
            id INT PRIMARY KEY AUTO_INCREMENT,
            story_id INT NOT NULL,
            tag_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
            UNIQUE KEY unique_story_tag (story_id, tag_id)
        )
        """
        cursor.execute(story_tags_table)
        print("✅ Story tags junction table created")
        
        # 6. Create story_views table
        print("📝 Creating story_views table...")
        story_views_table = """
        CREATE TABLE IF NOT EXISTS story_views (
            id INT PRIMARY KEY AUTO_INCREMENT,
            story_id INT NOT NULL,
            user_id INT NULL,
            ip_address VARCHAR(45),
            user_agent TEXT,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            INDEX idx_story_id (story_id),
            INDEX idx_viewed_at (viewed_at)
        )
        """
        cursor.execute(story_views_table)
        print("✅ Story views table created")
        
        # 7. Create story_likes table
        print("📝 Creating story_likes table...")
        story_likes_table = """
        CREATE TABLE IF NOT EXISTS story_likes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            story_id INT NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_story_like (story_id, user_id)
        )
        """
        cursor.execute(story_likes_table)
        print("✅ Story likes table created")
        
        # 8. Create story_comments table
        print("📝 Creating story_comments table...")
        story_comments_table = """
        CREATE TABLE IF NOT EXISTS story_comments (
            id INT PRIMARY KEY AUTO_INCREMENT,
            story_id INT NOT NULL,
            user_id INT NOT NULL,
            parent_id INT NULL,
            content TEXT NOT NULL,
            status ENUM('published', 'pending', 'hidden') DEFAULT 'published',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (parent_id) REFERENCES story_comments(id) ON DELETE CASCADE,
            INDEX idx_story_id (story_id),
            INDEX idx_created_at (created_at)
        )
        """
        cursor.execute(story_comments_table)
        print("✅ Story comments table created")
        
        connection.commit()
        print("\n🎉 All tables created successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def insert_default_data():
    """Insert default categories and tags"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        print("\n📊 Inserting default data...")
        
        # Insert tag categories
        print("📝 Inserting tag categories...")
        categories = [
            ('Genre', 'Story genres and types', '#007bff', 'fas fa-book'),
            ('Mood', 'Emotional tone and atmosphere', '#28a745', 'fas fa-heart'),
            ('Theme', 'Central themes and topics', '#ffc107', 'fas fa-lightbulb'),
            ('Audience', 'Target audience and age groups', '#17a2b8', 'fas fa-users'),
            ('Length', 'Story length categories', '#6f42c1', 'fas fa-clock'),
            ('Setting', 'Time period and location', '#fd7e14', 'fas fa-map-marker-alt')
        ]
        
        category_query = "INSERT IGNORE INTO tag_categories (name, description, color, icon) VALUES (%s, %s, %s, %s)"
        cursor.executemany(category_query, categories)
        print("✅ Tag categories inserted")
        
        # Insert tags for each category
        print("📝 Inserting tags...")
        tags_data = [
            # Genre tags (category_id = 1)
            ('Adventure', 1, 'Exciting journeys and quests'),
            ('Romance', 1, 'Love stories and relationships'),
            ('Fantasy', 1, 'Magical and supernatural elements'),
            ('Mystery', 1, 'Puzzles and unknown elements'),
            ('Comedy', 1, 'Humorous and funny stories'),
            ('Drama', 1, 'Serious and emotional narratives'),
            
            # Mood tags (category_id = 2)
            ('Happy', 2, 'Joyful and uplifting stories'),
            ('Sad', 2, 'Melancholic and emotional stories'),
            ('Inspiring', 2, 'Motivational and uplifting content'),
            ('Dark', 2, 'Serious and somber tone'),
            ('Lighthearted', 2, 'Fun and carefree atmosphere'),
            ('Suspenseful', 2, 'Tense and exciting mood'),
            
            # Theme tags (category_id = 3)
            ('Family', 3, 'Family relationships and bonds'),
            ('Friendship', 3, 'Bonds between friends'),
            ('Love', 3, 'Romantic and platonic love'),
            ('Growth', 3, 'Personal development and coming of age'),
            ('Adventure', 3, 'Exploration and discovery'),
            ('Life Lessons', 3, 'Moral and educational themes'),
            
            # Audience tags (category_id = 4)
            ('Children', 4, 'Suitable for young children (0-12)'),
            ('Teens', 4, 'For teenage readers (13-17)'),
            ('Young Adults', 4, 'For young adults (18-25)'),
            ('Adults', 4, 'Mature content for adults (25+)'),
            ('Family', 4, 'Appropriate for all ages'),
            ('Educational', 4, 'Learning and instructional content'),
            
            # Length tags (category_id = 5)
            ('Very Short', 5, 'Under 500 words'),
            ('Short', 5, '500-2000 words'),
            ('Medium', 5, '2000-5000 words'),
            ('Long', 5, '5000-10000 words'),
            ('Very Long', 5, '10000+ words'),
            ('Series', 5, 'Multi-part story series'),
            
            # Setting tags (category_id = 6)
            ('Modern', 6, 'Contemporary present day'),
            ('Historical', 6, 'Past time periods'),
            ('Future', 6, 'Futuristic or sci-fi setting'),
            ('Fantasy World', 6, 'Imaginary or magical realms'),
            ('Urban', 6, 'City and metropolitan areas'),
            ('Nature', 6, 'Countryside, forests, outdoors')
        ]
        
        tag_query = "INSERT IGNORE INTO tags (name, category_id, description) VALUES (%s, %s, %s)"
        cursor.executemany(tag_query, tags_data)
        print("✅ Default tags inserted")
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"❌ Error inserting default data: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def show_table_summary():
    """Show summary of created tables"""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        print("\n" + "="*50)
        print("📋 DATABASE SETUP SUMMARY")
        print("="*50)
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"📊 Total Tables: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   🔹 {table_name}: {count} records")
        
        print("\n✅ Database setup completed successfully!")
        print("🚀 Ready to run insert_test_data.py!")
        
    except Error as e:
        print(f"❌ Error getting table summary: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    """Main execution function"""
    print("🚀 AI STORYTELLING PLATFORM - SIMPLIFIED DATABASE SETUP")
    print("="*55)
    
    # Create all tables
    if not create_all_tables():
        print("❌ Failed to create tables!")
        return
    
    # Insert default data
    if not insert_default_data():
        print("❌ Failed to insert default data!")
        return
    
    # Show summary
    show_table_summary()

if __name__ == "__main__":
    main()