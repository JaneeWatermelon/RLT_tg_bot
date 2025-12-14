CREATE TABLE IF NOT EXISTS video_snapshots (
    id VARCHAR UNIQUE NOT NULL,
    video_id VARCHAR REFERENCES videos(id),

    views_count BIGINT CHECK (views_count >= 0),
    likes_count BIGINT CHECK (views_count >= 0),
    comments_count BIGINT CHECK (views_count >= 0),
    reports_count BIGINT CHECK (views_count >= 0),

    delta_views_count BIGINT,
    delta_likes_count BIGINT,
    delta_comments_count BIGINT,
    delta_reports_count BIGINT,
    
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON video_snapshots(created_at);
CREATE INDEX IF NOT EXISTS idx_snapshots_video_id ON video_snapshots(video_id);
