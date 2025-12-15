import json
import os
import asyncio
import time

import psycopg2
import core.database as database
import dotenv

def wait_for_db(dsn, retries=10, delay=2):
    for i in range(retries):
        try:
            psycopg2.connect(**dsn).close()
            return
        except psycopg2.OperationalError:
            print("DB not ready, retrying...")
            time.sleep(delay)
    raise RuntimeError("DB not available")

def main(db: database.Database):
    ASSETS_ROOT = os.getenv("ASSETS_ROOT")
    with open(os.path.join(ASSETS_ROOT, "videos.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    video_features = [
        "id", 
        "video_created_at",
        "views_count", 
        "likes_count", 
        "reports_count",
        "comments_count", 
        "creator_id", 
        "created_at", 
        "updated_at",
    ]
    video_snapshots_features = [
        "id", 
        "video_id", 

        "views_count", 
        "likes_count", 
        "comments_count",
        "reports_count", 

        "delta_views_count", 
        "delta_likes_count",
        "delta_reports_count", 
        "delta_comments_count", 

        "created_at",
        "updated_at",
    ]

    video_query = f"""
        INSERT INTO videos
        ({", ".join(video_features)})
        VALUES ({", ".join(["%s"] * len(video_features))})
        ON CONFLICT (id) DO NOTHING
        """
    video_snapshots_query = f"""
        INSERT INTO video_snapshots
        ({", ".join(video_snapshots_features)})
        VALUES ({", ".join(["%s"] * len(video_snapshots_features))})
        ON CONFLICT (id) DO NOTHING
        """

    for video in data["videos"]:
        video_params = list(video.get(key) for key in video_features)
        db.execute(query=video_query, params=video_params)

        video_snapshots_data = []
        for snap in video["snapshots"]:
            video_snapshots_params = list(snap.get(key) for key in video_snapshots_features)
            video_snapshots_data.append((video_snapshots_query, video_snapshots_params))
        
        db.execute_many(data=video_snapshots_data)

if __name__ == "__main__":
    dotenv.load_dotenv("dev.env")

    params = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    wait_for_db(params)

    db = database.Database(**params)

    main(db)

    print("Data loaded successfully!")
