import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def create_database():
    """Create database and tables with improved error handling"""
    database = None
    cursor = None
    
    try:
        # Connect without specifying database first
        database = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        cursor = database.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS crowd_detection_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("USE crowd_detection_system")
        
        # Users table with improved security
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_username (username),
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # User videos table with better metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_videos (
                video_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                original_filename VARCHAR(255) NOT NULL,
                stored_filename VARCHAR(500) NOT NULL,
                file_size BIGINT,
                duration FLOAT,
                resolution VARCHAR(20),
                file_format VARCHAR(10),
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('uploaded', 'processing', 'completed', 'failed') DEFAULT 'uploaded',
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_upload_time (upload_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Detection results with comprehensive analytics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_results (
                result_id INT AUTO_INCREMENT PRIMARY KEY,
                video_id INT NOT NULL,
                total_frames INT NOT NULL,
                processed_frames INT NOT NULL,
                crowd_events INT DEFAULT 0,
                max_crowd_size INT DEFAULT 0,
                average_crowd_size FLOAT DEFAULT 0.0,
                high_density_alerts INT DEFAULT 0,
                video_duration FLOAT DEFAULT 0.0,
                processing_time FLOAT DEFAULT 0.0,
                fps FLOAT DEFAULT 0.0,
                resolution VARCHAR(20),
                result_data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES user_videos(video_id) ON DELETE CASCADE,
                INDEX idx_video_id (video_id),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # User activities with enhanced logging
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_activities (
                activity_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                activity_type ENUM('register', 'login', 'upload', 'process', 'download', 'logout', 'error') NOT NULL,
                activity_details TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                success BOOLEAN DEFAULT TRUE,
                error_message TEXT,
                activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                INDEX idx_user_activity (user_id, activity_type),
                INDEX idx_activity_time (activity_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # System settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                setting_id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        database.commit()
        logger.info("✅ Database and tables created successfully!")
        
        # Insert default settings
        cursor.execute("""
            INSERT IGNORE INTO system_settings (setting_key, setting_value, description) 
            VALUES 
            ('min_crowd_size', '3', 'Minimum number of people to consider as crowd'),
            ('max_upload_size', '524288000', 'Maximum upload file size in bytes'),
            ('allowed_formats', 'mp4,avi,mov,mkv,wmv', 'Allowed video formats'),
            ('analysis_timeout', '300', 'Maximum analysis time in seconds')
        """)
        database.commit()
        
    except Error as e:
        logger.error(f"❌ Database creation failed: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if database and database.is_connected():
            database.close()

def get_database_connection():
    """Get database connection with error handling"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'crowd_detection_system'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            connection_timeout=30,
            autocommit=False
        )
        return connection
    except Error as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

if __name__ == "__main__":
    create_database()