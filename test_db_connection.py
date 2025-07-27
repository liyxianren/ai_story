import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def test_database_connection():
    """
    Test the MySQL database connection using the provided credentials
    """
    try:
        # Get connection parameters from environment variables or use defaults
        host = os.environ.get('PORT_FORWARDED_HOSTNAME', 'localhost')
        port = os.environ.get('DATABASE_PORT_FORWARDED_PORT', '3306')
        user = 'root'
        password = '69uc42U0oG7Js5Cm831ylixRqHODwXLI'
        database = 'zeabur'
        
        print("🔄 Attempting to connect to MySQL database...")
        print(f"Host: {host}")
        print(f"Port: {port}")
        print(f"User: {user}")
        print(f"Database: {database}")
        print("-" * 50)
        
        # Create connection
        connection = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            connection_timeout=10
        )
        
        if connection.is_connected():
            # Get server info
            db_info = connection.get_server_info()
            print(f"✅ Successfully connected to MySQL Server version: {db_info}")
            
            # Create cursor and execute a test query
            cursor = connection.cursor()
            
            # Test basic query
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 Database version: {version[0]}")
            
            # Show current database
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()
            print(f"🗄️  Current database: {current_db[0]}")
            
            # Show tables in the database
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📋 Tables in '{database}' database:")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print(f"📭 No tables found in '{database}' database")
            
            cursor.close()
            print("\n✅ Database connection test completed successfully!")
            return True
            
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔌 MySQL connection is closed")

def main():
    """
    Main function to run the database connection test
    """
    print("🚀 MySQL Database Connection Test")
    print("=" * 50)
    
    # Check if environment variables are set
    if not os.environ.get('PORT_FORWARDED_HOSTNAME'):
        print("⚠️  Warning: PORT_FORWARDED_HOSTNAME environment variable not set")
        print("   Using 'localhost' as default")
    
    if not os.environ.get('DATABASE_PORT_FORWARDED_PORT'):
        print("⚠️  Warning: DATABASE_PORT_FORWARDED_PORT environment variable not set")
        print("   Using '3306' as default")
    
    print()
    
    # Test the connection
    success = test_database_connection()
    
    if success:
        print("\n🎉 Your database is ready for the website!")
    else:
        print("\n❌ Database connection failed. Please check your connection details.")

if __name__ == "__main__":
    main() 