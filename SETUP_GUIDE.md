# TrendAI Setup Guide

Complete guide to get TrendAI running on your system.

## Quick Start (5 minutes)

### Step 1: Database (Already Done)
The PostgreSQL database is already set up in Supabase with all necessary tables.

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python integrated_api.py
```

Server will start at: http://localhost:8000

### Step 3: Frontend Setup

```bash
# In the project root directory
npm install

# Start the frontend
npm run dev
```

Frontend will open at: http://localhost:5173

### Step 4: Use the Platform

1. Open http://localhost:5173 in your browser
2. Enter a token symbol (e.g., BTC, ETH, DOGE)
3. Get instant risk analysis

## Detailed Setup

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- pip (Python package manager)
- npm (Node package manager)

### Backend Components

#### 1. ML Model Training (Optional)

If you have training data in `data/big_posts.csv`:

```bash
python backend/train_classifier.py
```

This creates `bot_detector.pkl` which the API uses for predictions.

#### 2. Data Loading (Optional)

If you have CSV files with existing analysis:

```bash
python backend/data_loader.py
```

This loads your CSV data into Supabase tables.

#### 3. API Server

```bash
python backend/integrated_api.py
```

Or use the provided script:

```bash
chmod +x backend/start.sh
./backend/start.sh
```

### Frontend Setup

```bash
# Install all dependencies
npm install

# Development server (with hot reload)
npm run dev

# Production build
npm run build
npm run preview
```

### Environment Variables

The system uses Supabase environment variables that are automatically configured:

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key for backend operations

These are already set up in your environment.

## Testing the System

### 1. Health Check

```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "status": "active",
  "version": "3.0",
  "components": {
    "ai_model": true,
    "database": "Supabase",
    "agent": "Active"
  }
}
```

### 2. Analyze a Post

```bash
curl -X POST http://localhost:8000/analyze/post \
  -H "Content-Type: application/json" \
  -d '{"text": "BUY NOW!!! 1000x MOON SOON!!!"}'
```

### 3. Check Token Risk

```bash
curl http://localhost:8000/analyze/token/BTC
```

## Data Requirements

### For Training (Optional)

If training your own model, you need `data/big_posts.csv` with columns:
- `post_id`: Unique identifier
- `text`: Post content
- `type`: organic/bot/coordinated/fake_news
- `token_id`: Token symbol

### For Analysis (Optional)

For pre-existing analysis, you need:

1. `big_posts_enriched.csv`: Posts with sentiment scores
2. `final_risk_scores.csv`: Token risk calculations
3. `final_narrative_risk.csv`: Narrative analysis
4. `final_account_trust.csv`: Account trust scores

## Troubleshooting

### Backend Issues

**Problem**: "Module not found" errors

**Solution**:
```bash
pip install -r backend/requirements.txt
```

**Problem**: "bot_detector.pkl not found"

**Solution**: Either train the model or disable bot detection in the API.

### Frontend Issues

**Problem**: "Cannot connect to API"

**Solution**: Make sure backend is running on port 8000:
```bash
curl http://localhost:8000/
```

**Problem**: CORS errors

**Solution**: CORS is configured in `integrated_api.py`. Verify the frontend URL is correct.

### Database Issues

**Problem**: "No data available"

**Solution**: Run the data loader:
```bash
python backend/data_loader.py
```

Or manually add test data to Supabase.

## API Documentation

Once the backend is running, visit:
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## File Structure

```
TrendAI/
├── backend/
│   ├── integrated_api.py       # Main API server
│   ├── analysis_agent.py       # Explanation generator
│   ├── train_classifier.py     # ML training
│   ├── risk_engine_v2.py       # Risk calculation
│   ├── narrative_risk.py       # Narrative analysis
│   ├── data_loader.py          # Data import script
│   ├── requirements.txt        # Python dependencies
│   └── start.sh                # Startup script
├── src/
│   ├── App.tsx                 # Main application
│   ├── components/
│   │   ├── TokenAnalyzer.tsx   # Token analysis UI
│   │   ├── PostChecker.tsx     # Post verification UI
│   │   └── Dashboard.tsx       # Statistics dashboard
│   └── index.css               # Styles
├── package.json                # Node dependencies
└── README.md                   # Documentation
```

## Production Deployment

### Backend

1. Use a production WSGI server:
```bash
pip install gunicorn
gunicorn backend.integrated_api:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Set up environment variables securely

3. Use a reverse proxy (nginx) for HTTPS

### Frontend

```bash
npm run build
```

Deploy the `dist/` folder to any static hosting service.

### Database

Supabase is production-ready. Enable:
- Connection pooling
- Automatic backups
- Monitoring

## Support

For issues or questions:
1. Check the API docs at http://localhost:8000/docs
2. Review logs in the terminal
3. Verify database connection in Supabase dashboard

## Next Steps

1. Add more training data to improve model accuracy
2. Implement real-time data collection from social media
3. Add email alerts for high-risk tokens
4. Create mobile app version
5. Add historical trend analysis
