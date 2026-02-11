from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import json
from data_handler import DataHandler

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize data handler
data_handler = DataHandler()

@app.route('/')
def home():
    return jsonify({
        "message": "Brent Oil Prices Analysis API",
        "version": "1.0",
        "endpoints": [
            "/api/prices",
            "/api/prices/<start_date>/<end_date>",
            "/api/change_points",
            "/api/events",
            "/api/event_correlation/<event_id>",
            "/api/volatility",
            "/api/summary_stats"
        ]
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data"""
    try:
        prices_data = data_handler.get_price_data()
        return jsonify(prices_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prices/<start_date>/<end_date>', methods=['GET'])
def get_prices_by_date(start_date, end_date):
    """Get price data for specific date range"""
    try:
        filtered_data = data_handler.filter_by_date(start_date, end_date)
        return jsonify(filtered_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/change_points', methods=['GET'])
def get_change_points():
    """Get detected change points from analysis"""
    try:
        change_points = data_handler.get_change_points()
        return jsonify(change_points)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get geopolitical and economic events"""
    try:
        events = data_handler.get_events()
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/event_correlation/<event_id>', methods=['GET'])
def get_event_correlation(event_id):
    """Get price impact analysis for specific event"""
    try:
        correlation = data_handler.get_event_correlation(event_id)
        return jsonify(correlation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """Get volatility metrics"""
    try:
        volatility_data = data_handler.calculate_volatility()
        return jsonify(volatility_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summary_stats', methods=['GET'])
def get_summary_stats():
    """Get summary statistics"""
    try:
        stats = data_handler.get_summary_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/price_impact', methods=['POST'])
def calculate_price_impact():
    """Calculate price impact around specific dates"""
    try:
        data = request.get_json()
        event_date = data.get('event_date')
        window_days = data.get('window_days', 30)
        
        impact = data_handler.calculate_price_impact(event_date, window_days)
        return jsonify(impact)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)