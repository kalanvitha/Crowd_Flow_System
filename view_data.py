import mysql.connector
from dotenv import load_dotenv
import os
import json
from tabulate import tabulate

load_dotenv()

def view_database_data():
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'kalanvitha'),
            database=os.getenv('DB_NAME', 'crowd_detection_system')
        )
        
        cursor = conn.cursor(dictionary=True)
        
        print("=" * 50)
        print("CROWD DETECTION SYSTEM - DATABASE VIEWER")
        print("=" * 50)
        
        # 1. View Users
        print("\n📊 USERS TABLE:")
        cursor.execute("SELECT user_id, username, email, created_at FROM users")
        users = cursor.fetchall()
        print(tabulate(users, headers="keys", tablefmt="grid"))
        
        # 2. View Videos
        print("\n🎥 VIDEOS TABLE:")
        cursor.execute("""
            SELECT video_id, user_id, original_filename, file_size, 
                   upload_time, status 
            FROM user_videos 
            ORDER BY upload_time DESC
        """)
        videos = cursor.fetchall()
        print(tabulate(videos, headers="keys", tablefmt="grid"))
        
        # 3. View Results
        print("\n📈 ANALYSIS RESULTS:")
        cursor.execute("""
            SELECT result_id, video_id, total_frames, max_crowd_size,
                   high_density_alerts, processing_time, created_at
            FROM detection_results 
            ORDER BY created_at DESC
        """)
        results = cursor.fetchall()
        print(tabulate(results, headers="keys", tablefmt="grid"))
        
        # 4. View Complete Analysis Data
        print("\n🔍 DETAILED ANALYSIS DATA:")
        cursor.execute("""
            SELECT 
                u.username,
                uv.original_filename,
                uv.upload_time,
                dr.total_frames,
                dr.processed_frames,
                dr.max_crowd_size,
                dr.average_crowd_size,
                dr.high_density_alerts,
                dr.processing_time,
                dr.created_at as analysis_time
            FROM users u
            JOIN user_videos uv ON u.user_id = uv.user_id
            JOIN detection_results dr ON uv.video_id = dr.video_id
            ORDER BY uv.upload_time DESC
            LIMIT 5
        """)
        detailed_results = cursor.fetchall()
        print(tabulate(detailed_results, headers="keys", tablefmt="grid"))
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_database_data()