# Brent Oil Prices Analysis - Backend API

## Setup Instructions

1. Install Python 3.8 or higher
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   Install dependencies:

bash
pip install -r requirements.txt
Run the Flask application:

bash
python app.py
The API will be available at http://localhost:5000

API Endpoints
GET / - API information

GET /api/prices - Historical price data

GET /api/change_points - Detected change points

GET /api/events - Geopolitical events

GET /api/volatility - Volatility metrics

GET /api/summary_stats - Summary statistics

POST /api/price_impact - Calculate price impact