CREATE TABLE IF NOT EXISTS videos (
    id VARCHAR UNIQUE NOT NULL,
    creator_id VARCHAR NOT NULL,
    video_created_at TIMESTAMP NOT NULL,
    views_count BIGINT DEFAULT 0 CHECK (views_count >= 0),
    likes_count BIGINT DEFAULT 0 CHECK (likes_count >= 0),
    comments_count BIGINT DEFAULT 0 CHECK (comments_count >= 0),
    reports_count BIGINT DEFAULT 0 CHECK (reports_count >= 0),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
