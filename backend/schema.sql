-- TrendAI Schema - Version locale (sans Supabase/RLS)

DROP TABLE IF EXISTS analysis_reports CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS tokens CASCADE;
DROP TABLE IF EXISTS narratives CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;

CREATE TABLE posts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id text NOT NULL,
    token_id text NOT NULL,
    text text NOT NULL,
    post_type text DEFAULT 'organic',
    is_bot boolean DEFAULT false,
    sentiment_score double precision DEFAULT 0,
    sentiment_label text DEFAULT 'Neutral',
    created_at timestamptz DEFAULT now()
);

CREATE TABLE tokens (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    token_id text UNIQUE NOT NULL,
    name text,
    risk_score double precision DEFAULT 0,
    risk_label text DEFAULT 'SAFE',
    bot_ratio double precision DEFAULT 0,
    avg_sentiment double precision DEFAULT 0,
    total_posts integer DEFAULT 0,
    suspicious_posts integer DEFAULT 0,
    reason text DEFAULT '',
    last_analyzed timestamptz DEFAULT now()
);

CREATE TABLE narratives (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    narrative_id text NOT NULL,
    token_id text NOT NULL,
    topic text NOT NULL,
    risk_level text DEFAULT 'LOW',
    bot_percentage double precision DEFAULT 0,
    avg_sentiment double precision DEFAULT 0,
    warning text DEFAULT '',
    post_count integer DEFAULT 0,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE accounts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id text UNIQUE NOT NULL,
    username text NOT NULL,
    trust_score double precision DEFAULT 50,
    trust_label text DEFAULT 'NEUTRAL',
    bot_ratio double precision DEFAULT 0,
    total_posts integer DEFAULT 0,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE analysis_reports (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    token_id text NOT NULL,
    report_type text DEFAULT 'FULL_ANALYSIS',
    risk_score double precision NOT NULL,
    risk_label text NOT NULL,
    explanation text NOT NULL,
    key_findings jsonb DEFAULT '[]',
    recommendations text DEFAULT '',
    created_at timestamptz DEFAULT now()
);

CREATE INDEX idx_posts_token_id ON posts(token_id);
CREATE INDEX idx_tokens_token_id ON tokens(token_id);
CREATE INDEX idx_narratives_token_id ON narratives(token_id);