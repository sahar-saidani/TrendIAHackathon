# TrendAI - Token Intelligence Platform

TrendAI is an AI-powered platform that helps crypto investors detect fake news, bot manipulation, and coordinated campaigns around cryptocurrency tokens.

## Features

- **Token Analysis**: Get comprehensive risk analysis for any cryptocurrency token
- **Post Checker**: Analyze individual social media posts for bot activity and manipulation
- **Dashboard**: View real-time statistics and high-risk tokens
- **AI-Powered Detection**: Machine learning model trained to detect bot and coordinated campaigns
- **Professional Reports**: Plain-language explanations designed for investors, not technical experts

## Architecture

### Backend (FastAPI + Python)
- **integrated_api.py**: Main API server with Supabase integration
- **analysis_agent.py**: Intelligent agent that generates investor-friendly explanations
- **train_classifier.py**: ML model training script
- **risk_engine_v2.py**: Advanced risk calculation engine
- **narrative_risk.py**: Narrative manipulation detection
- **data_loader.py**: Script to load CSV data into Supabase

### Frontend (React + TypeScript)
- **TokenAnalyzer**: Main interface for analyzing tokens
- **PostChecker**: Check individual posts for manipulation
- **Dashboard**: Real-time statistics and high-risk token monitoring

### Database (Supabase/PostgreSQL)
- `posts`: Social media posts with AI analysis
- `tokens`: Token risk profiles
- `narratives`: Detected narrative campaigns
- `accounts`: User trust scores
- `analysis_reports`: Historical analysis reports

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- Supabase account (database is already set up)

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Train the ML model (if you have training data)
python train_classifier.py

# Load data into Supabase (if you have CSV files)
python data_loader.py

# Start the API server
python integrated_api.py
```

The API will run on http://localhost:8000

### 3. Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on http://localhost:5173

## Usage

### For Investors

1. **Check a Token**:
   - Go to Token Analyzer
   - Enter a token symbol (e.g., BTC, ETH)
   - Get instant risk analysis with plain-language explanation

2. **Check a Post**:
   - Go to Post Checker
   - Paste any social media post
   - See if it's genuine or part of a manipulation campaign

3. **Monitor Risks**:
   - Go to Dashboard
   - View high-risk tokens and overall statistics

### API Endpoints

- `GET /` - Health check
- `POST /analyze/post` - Analyze a single post
- `GET /analyze/token/{token_id}` - Complete token analysis
- `GET /token/{token_id}/history` - Historical reports
- `GET /dashboard/high-risk` - High-risk tokens
- `GET /dashboard/statistics` - Overall statistics

## How It Works

1. **Data Collection**: Social media posts about crypto tokens are collected
2. **AI Analysis**: Machine learning model classifies posts as organic or bot-generated
3. **Sentiment Analysis**: VADER sentiment analysis detects emotional manipulation
4. **Risk Calculation**: Combines bot detection, sentiment, and volume metrics
5. **Narrative Detection**: Identifies coordinated campaign topics
6. **Report Generation**: Analysis agent creates investor-friendly explanations

## Risk Levels

- **SAFE**: Normal organic community activity
- **SUSPICIOUS**: Moderate bot activity detected
- **HIGH RISK**: Significant manipulation detected
- **PUMP & DUMP**: Coordinated artificial hype campaign
- **FUD ATTACK**: Coordinated negative campaign

## Environment Variables

The following environment variables are automatically configured:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key

## Data Files (Optional)

If you have these CSV files, you can load them into the database:
- `big_posts_enriched.csv`: Social media posts with analysis
- `final_risk_scores.csv`: Token risk scores
- `final_narrative_risk.csv`: Narrative risk data
- `final_account_trust.csv`: Account trust scores
- `bot_detector.pkl`: Trained ML model

## Tech Stack

- **Backend**: FastAPI, Python, scikit-learn, NLTK, pandas
- **Frontend**: React, TypeScript, Tailwind CSS, Lucide Icons
- **Database**: Supabase (PostgreSQL)
- **ML**: Logistic Regression with TF-IDF vectorization
- **NLP**: VADER sentiment analysis

## Security

- All database tables use Row Level Security (RLS)
- Public read access for analysis results
- Authenticated write access for data ingestion
- No sensitive data exposed to frontend

## License

MIT

## Support

For questions or issues, please check the API documentation at http://localhost:8000/docs when the server is running.
