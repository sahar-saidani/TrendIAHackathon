/*
  # TrendAI Database Schema
  
  1. New Tables
    - `posts`
      - `id` (uuid, primary key) - Unique post identifier
      - `post_id` (text) - Original post ID from data
      - `token_id` (text) - Token being discussed
      - `text` (text) - Post content
      - `post_type` (text) - Type: organic, bot, coordinated, fake_news
      - `is_bot` (boolean) - AI classification result
      - `sentiment_score` (float) - Sentiment analysis (-1 to 1)
      - `sentiment_label` (text) - Positive, Negative, or Neutral
      - `created_at` (timestamptz) - Timestamp
      
    - `tokens`
      - `id` (uuid, primary key)
      - `token_id` (text, unique) - Token symbol (e.g., BTC, ETH)
      - `name` (text) - Token name
      - `risk_score` (float) - Overall risk score (0-100)
      - `risk_label` (text) - SAFE, SUSPICIOUS, HIGH RISK, PUMP & DUMP, FUD ATTACK
      - `bot_ratio` (float) - Percentage of bot activity
      - `avg_sentiment` (float) - Average sentiment
      - `total_posts` (integer) - Total posts analyzed
      - `suspicious_posts` (integer) - Number of suspicious posts
      - `reason` (text) - Risk explanation
      - `last_analyzed` (timestamptz) - Last analysis timestamp
      
    - `narratives`
      - `id` (uuid, primary key)
      - `narrative_id` (text) - Narrative identifier
      - `token_id` (text) - Associated token
      - `topic` (text) - Narrative topic/theme
      - `risk_level` (text) - LOW, HIGH, CRITICAL
      - `bot_percentage` (float) - Bot activity in this narrative
      - `avg_sentiment` (float) - Average sentiment
      - `warning` (text) - Warning message
      - `post_count` (integer) - Number of posts in narrative
      - `created_at` (timestamptz)
      
    - `accounts`
      - `id` (uuid, primary key)
      - `account_id` (text, unique) - Account identifier
      - `username` (text) - Display name
      - `trust_score` (float) - Trust score (0-100)
      - `trust_label` (text) - TRUSTED, NEUTRAL, SUSPICIOUS, BOT
      - `bot_ratio` (float) - Percentage of bot-like posts
      - `total_posts` (integer) - Total posts by this account
      - `created_at` (timestamptz)
      
    - `analysis_reports`
      - `id` (uuid, primary key)
      - `token_id` (text) - Token analyzed
      - `report_type` (text) - FULL_ANALYSIS, QUICK_CHECK
      - `risk_score` (float) - Risk score
      - `risk_label` (text) - Risk classification
      - `explanation` (text) - Professional explanation in plain language
      - `key_findings` (jsonb) - Structured findings
      - `recommendations` (text) - Investor recommendations
      - `created_at` (timestamptz)
      
  2. Security
    - Enable RLS on all tables
    - Add policies for public read access (this is a public analysis tool)
    - Add policies for authenticated write access (for data ingestion)
*/

-- Posts Table
-- Tables pour TrendAI (version locale sans RLS/policies)

-- Posts Table
CREATE TABLE IF NOT EXISTS posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id text NOT NULL,
  token_id text NOT NULL,
  text text NOT NULL,
  post_type text DEFAULT 'organic',
  is_bot boolean DEFAULT false,
  sentiment_score float DEFAULT 0,
  sentiment_label text DEFAULT 'Neutral',
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_posts_token_id ON posts(token_id);

-- Tokens Table
CREATE TABLE IF NOT EXISTS tokens (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token_id text UNIQUE NOT NULL,
  name text,
  risk_score float DEFAULT 0,
  risk_label text DEFAULT 'SAFE',
  bot_ratio float DEFAULT 0,
  avg_sentiment float DEFAULT 0,
  total_posts integer DEFAULT 0,
  suspicious_posts integer DEFAULT 0,
  reason text DEFAULT '',
  last_analyzed timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tokens_token_id ON tokens(token_id);

-- Narratives Table
CREATE TABLE IF NOT EXISTS narratives (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  narrative_id text NOT NULL,
  token_id text NOT NULL,
  topic text NOT NULL,
  risk_level text DEFAULT 'LOW',
  bot_percentage float DEFAULT 0,
  avg_sentiment float DEFAULT 0,
  warning text DEFAULT '',
  post_count integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_narratives_token_id ON narratives(token_id);

-- Accounts Table
CREATE TABLE IF NOT EXISTS accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id text UNIQUE NOT NULL,
  username text NOT NULL,
  trust_score float DEFAULT 50,
  trust_label text DEFAULT 'NEUTRAL',
  bot_ratio float DEFAULT 0,
  total_posts integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Analysis Reports Table
CREATE TABLE IF NOT EXISTS analysis_reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token_id text NOT NULL,
  report_type text DEFAULT 'FULL_ANALYSIS',
  risk_score float NOT NULL,
  risk_label text NOT NULL,
  explanation text NOT NULL,
  key_findings jsonb DEFAULT '[]'::jsonb,
  recommendations text DEFAULT '',
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_reports_token_id ON analysis_reports(token_id);
CREATE INDEX IF NOT EXISTS idx_reports_created_at ON analysis_reports(created_at DESC);