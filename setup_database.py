import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Setup database and tables manually"""
    try:
        # Connect to MySQL server without specifying database first
        database = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'kalanvitha'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        cursor = database.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS crowd_detection_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("USE crowd_detection_system")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100),
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Create videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_videos (
                video_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                original_filename VARCHAR(255),
                stored_filename VARCHAR(500),
                file_size BIGINT,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                video_duration FLOAT DEFAULT 0,
                video_resolution VARCHAR(50),
                status ENUM('uploaded', 'processing', 'completed', 'failed') DEFAULT 'uploaded',
                INDEX idx_user_id (user_id),
                INDEX idx_upload_time (upload_time)
            )
        """)
        
        # Create results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_results (
                result_id INT AUTO_INCREMENT PRIMARY KEY,
                video_id INT,
                total_frames INT,
                processed_frames INT,
                crowd_events INT,
                max_crowd_size INT,
                average_crowd_size FLOAT,
                high_density_alerts INT,
                video_duration FLOAT,
                processing_time FLOAT,
                fps FLOAT,
                resolution VARCHAR(50),
                result_data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_video_id (video_id),
                INDEX idx_created_at (created_at)
            )
        """)
        
        database.commit()
        print("✅ Database and tables created successfully!")
        
        # Create a sample admin user (optional)
        try:
            import bcrypt
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT IGNORE INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                ("admin", "admin@crowddetection.com", hashed_password)
            )
            database.commit()
            print("✅ Sample admin user created: admin / admin123")
        except Exception as e:
            print(f"⚠️ Could not create sample user: {e}")
        
    except Error as e:
        print(f"❌ Database setup failed: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'database' in locals():
            database.close()

if __name__ == '__main__':
    setup_database()