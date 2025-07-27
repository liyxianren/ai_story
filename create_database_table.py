import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_users_table():
    """
    Create the users table in the MySQL database
    """
    try:
        # Database connection
        connection = mysql.connector.connect(
            host='tpe1.clusters.zeabur.com',
            port=32149,
            user='root',
            password='69uc42U0oG7Js5Cm831ylixRqHODwXLI',
            database='zeabur'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create users table
            create_table_query = """
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
            );
            """
            
            cursor.execute(create_table_query)
            print("✅ Users table created successfully!")
            
            # Show table structure
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            
            print("\n📋 Users table structure:")
            for column in columns:
                print(f"   - {column[0]} ({column[1]})")
            
            cursor.close()
            connection.commit()
            return True
            
    except Error as e:
        print(f"❌ Error creating table: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    print("🚀 Creating Users Table")
    print("=" * 40)
    create_users_table() 