import mysql.connector
from mysql.connector import Error

def test_connection():
    """
    Simple database connection test
    MODIFY THE VALUES BELOW WITH YOUR ACTUAL DATABASE DETAILS
    """
    
    # ✅ ACTUAL DATABASE DETAILS (WORKING!)
    HOST = "tpe1.clusters.zeabur.com"  # Your Zeabur database hostname
    PORT = "32149"                     # Your Zeabur database port
    USER = "root"
    PASSWORD = "69uc42U0oG7Js5Cm831ylixRqHODwXLI"
    DATABASE = "zeabur"
    
    print("🔄 Testing database connection...")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    print(f"Database: {DATABASE}")
    print("-" * 40)
    
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=int(PORT),
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            connection_timeout=10
        )
        
        if connection.is_connected():
            print("✅ SUCCESS! Database connection established!")
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 MySQL version: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Found {len(tables)} tables in the database")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple MySQL Connection Test")
    print("=" * 50)
    print("📝 Before running, edit this file and replace:")
    print("   - HOST with your actual hostname")
    print("   - PORT with your actual port number")
    print()
    
    if test_connection():
        print("\n🎉 Your database is ready for the web application!")
    else:
        print("\n❌ Please check your connection details and try again.") 