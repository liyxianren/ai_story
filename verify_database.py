#!/usr/bin/env python3
"""
Database Verification Script for AI Storytelling Platform
This script verifies all database tables, relationships, and data integrity
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime

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

def test_database_connection():
    """Test basic database connection"""
    print("🔌 Testing database connection...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ Database connection successful!")
        print(f"   MySQL Version: {version[0]}")
        return True
        
    except Error as e:
        print(f"❌ Database connection test failed: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def verify_table_structure():
    """Verify all required tables exist with correct structure"""
    print("\n📋 Verifying table structure...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    required_tables = [
        'users', 'tag_categories', 'tags', 'stories', 
        'story_tags', 'story_views', 'story_likes', 'story_comments'
    ]
    
    try:
        # Check if all tables exist
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        missing_tables = []
        for table in required_tables:
            if table not in existing_tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        else:
            print("✅ All required tables exist")
        
        # Check specific table structures
        structure_tests = {
            'users': ['id', 'username', 'email', 'password_hash'],
            'stories': ['id', 'user_id', 'title', 'content', 'language', 'status'],
            'tag_categories': ['id', 'name', 'description', 'color'],
            'tags': ['id', 'name', 'category_id', 'usage_count'],
            'story_tags': ['story_id', 'tag_id']
        }
        
        for table_name, required_columns in structure_tests.items():
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            
            missing_columns = [col for col in required_columns if col not in columns]
            if missing_columns:
                print(f"❌ Table {table_name} missing columns: {missing_columns}")
                return False
        
        print("✅ Table structures are correct")
        return True
        
    except Error as e:
        print(f"❌ Error verifying table structure: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def verify_foreign_key_relationships():
    """Verify foreign key relationships work correctly"""
    print("\n🔗 Verifying foreign key relationships...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Test stories -> users relationship
        cursor.execute("""
            SELECT s.id, s.title, u.username 
            FROM stories s 
            JOIN users u ON s.user_id = u.id 
            LIMIT 3
        """)
        story_users = cursor.fetchall()
        
        if story_users:
            print("✅ Stories -> Users relationship working")
            for story_id, title, username in story_users:
                print(f"   Story '{title}' by user '{username}'")
        else:
            print("⚠️  No story-user relationships found (may be expected if no test data)")
        
        # Test tags -> tag_categories relationship
        cursor.execute("""
            SELECT t.name, tc.name as category_name 
            FROM tags t 
            JOIN tag_categories tc ON t.category_id = tc.id 
            LIMIT 5
        """)
        tag_categories = cursor.fetchall()
        
        if tag_categories:
            print("✅ Tags -> Tag Categories relationship working")
            for tag_name, category_name in tag_categories:
                print(f"   Tag '{tag_name}' in category '{category_name}'")
        else:
            print("❌ No tag-category relationships found")
            return False
        
        # Test story_tags junction table
        cursor.execute("""
            SELECT s.title, t.name as tag_name, tc.name as category_name
            FROM story_tags st
            JOIN stories s ON st.story_id = s.id
            JOIN tags t ON st.tag_id = t.id
            JOIN tag_categories tc ON t.category_id = tc.id
            LIMIT 5
        """)
        story_tag_relations = cursor.fetchall()
        
        if story_tag_relations:
            print("✅ Story tags junction table working")
            for title, tag_name, category_name in story_tag_relations:
                print(f"   Story '{title}' tagged with '{tag_name}' ({category_name})")
        else:
            print("⚠️  No story-tag relationships found (may be expected if no test data)")
        
        return True
        
    except Error as e:
        print(f"❌ Error verifying foreign key relationships: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def verify_data_integrity():
    """Verify data integrity and constraints"""
    print("\n🔍 Verifying data integrity...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Check for duplicate usernames/emails
        cursor.execute("SELECT username, COUNT(*) FROM users GROUP BY username HAVING COUNT(*) > 1")
        duplicate_usernames = cursor.fetchall()
        
        cursor.execute("SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1")
        duplicate_emails = cursor.fetchall()
        
        if duplicate_usernames:
            print(f"❌ Duplicate usernames found: {duplicate_usernames}")
            return False
        
        if duplicate_emails:
            print(f"❌ Duplicate emails found: {duplicate_emails}")
            return False
        
        print("✅ No duplicate users found")
        
        # Check story status enum values
        cursor.execute("SELECT DISTINCT status FROM stories")
        story_statuses = [status[0] for status in cursor.fetchall()]
        valid_statuses = ['draft', 'pending', 'published', 'rejected', 'private', 'archived']
        
        invalid_statuses = [status for status in story_statuses if status not in valid_statuses]
        if invalid_statuses:
            print(f"❌ Invalid story statuses found: {invalid_statuses}")
            return False
        
        print("✅ Story statuses are valid")
        
        # Verify tag usage counts
        cursor.execute("""
            SELECT t.id, t.name, t.usage_count, COUNT(st.tag_id) as actual_usage
            FROM tags t
            LEFT JOIN story_tags st ON t.id = st.tag_id
            GROUP BY t.id, t.name, t.usage_count
            HAVING t.usage_count != COUNT(st.tag_id)
        """)
        incorrect_usage_counts = cursor.fetchall()
        
        if incorrect_usage_counts:
            print("⚠️  Tag usage counts may need updating:")
            for tag_id, tag_name, recorded_count, actual_count in incorrect_usage_counts:
                print(f"   Tag '{tag_name}': recorded={recorded_count}, actual={actual_count}")
        else:
            print("✅ Tag usage counts are accurate")
        
        return True
        
    except Error as e:
        print(f"❌ Error verifying data integrity: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def test_crud_operations():
    """Test basic CRUD operations"""
    print("\n⚙️  Testing CRUD operations...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Test CREATE - insert a test user
        test_user_data = (
            'test_user_' + str(int(datetime.now().timestamp())),
            'test@verification.com',
            'test_password_hash',
            'Test user for verification'
        )
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, bio) 
            VALUES (%s, %s, %s, %s)
        """, test_user_data)
        
        test_user_id = cursor.lastrowid
        print("✅ CREATE operation successful")
        
        # Test READ
        cursor.execute("SELECT username, email, bio FROM users WHERE id = %s", (test_user_id,))
        user_data = cursor.fetchone()
        
        if user_data and user_data[0] == test_user_data[0]:
            print("✅ READ operation successful")
        else:
            print("❌ READ operation failed")
            return False
        
        # Test UPDATE
        new_bio = "Updated bio for verification test"
        cursor.execute("UPDATE users SET bio = %s WHERE id = %s", (new_bio, test_user_id))
        
        cursor.execute("SELECT bio FROM users WHERE id = %s", (test_user_id,))
        updated_bio = cursor.fetchone()[0]
        
        if updated_bio == new_bio:
            print("✅ UPDATE operation successful")
        else:
            print("❌ UPDATE operation failed")
            return False
        
        # Test DELETE
        cursor.execute("DELETE FROM users WHERE id = %s", (test_user_id,))
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", (test_user_id,))
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            print("✅ DELETE operation successful")
        else:
            print("❌ DELETE operation failed")
            return False
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"❌ Error testing CRUD operations: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def generate_verification_report():
    """Generate a comprehensive verification report"""
    print("\n📊 GENERATING VERIFICATION REPORT")
    print("="*50)
    
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Database summary
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stories")
        total_stories = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tag_categories")
        total_categories = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM story_tags")
        total_story_tags = cursor.fetchone()[0]
        
        print(f"📈 Database Statistics:")
        print(f"   Users: {total_users}")
        print(f"   Stories: {total_stories}")
        print(f"   Tag Categories: {total_categories}")
        print(f"   Tags: {total_tags}")
        print(f"   Story-Tag Relationships: {total_story_tags}")
        
        # Story status distribution
        cursor.execute("SELECT status, COUNT(*) FROM stories GROUP BY status")
        status_distribution = cursor.fetchall()
        
        if status_distribution:
            print(f"\n📚 Story Status Distribution:")
            for status, count in status_distribution:
                print(f"   {status}: {count}")
        
        # Language distribution
        cursor.execute("SELECT language_name, COUNT(*) FROM stories GROUP BY language_name")
        language_distribution = cursor.fetchall()
        
        if language_distribution:
            print(f"\n🌍 Language Distribution:")
            for language, count in language_distribution:
                print(f"   {language}: {count}")
        
        # Most used tags
        cursor.execute("""
            SELECT t.name, tc.name as category, COUNT(st.tag_id) as usage_count
            FROM tags t
            JOIN tag_categories tc ON t.category_id = tc.id
            LEFT JOIN story_tags st ON t.id = st.tag_id
            GROUP BY t.id, t.name, tc.name
            ORDER BY usage_count DESC
            LIMIT 10
        """)
        popular_tags = cursor.fetchall()
        
        if popular_tags:
            print(f"\n🏷️  Most Used Tags:")
            for tag_name, category, usage_count in popular_tags:
                print(f"   {tag_name} ({category}): {usage_count} uses")
        
    except Error as e:
        print(f"❌ Error generating report: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    """Main verification function"""
    print("🔍 AI STORYTELLING PLATFORM - DATABASE VERIFICATION")
    print("="*55)
    
    all_tests_passed = True
    
    # Test database connection
    if not test_database_connection():
        all_tests_passed = False
    
    # Verify table structure
    if not verify_table_structure():
        all_tests_passed = False
    
    # Verify foreign key relationships
    if not verify_foreign_key_relationships():
        all_tests_passed = False
    
    # Verify data integrity
    if not verify_data_integrity():
        all_tests_passed = False
    
    # Test CRUD operations
    if not test_crud_operations():
        all_tests_passed = False
    
    # Generate comprehensive report
    generate_verification_report()
    
    print("\n" + "="*55)
    if all_tests_passed:
        print("✅ ALL VERIFICATION TESTS PASSED!")
        print("🎉 Database is ready for production use!")
    else:
        print("❌ Some verification tests failed!")
        print("⚠️  Please review the issues above before proceeding.")
    
    print("="*55)

if __name__ == "__main__":
    main()