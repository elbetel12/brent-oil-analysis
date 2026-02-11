import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class DataHandler:
    def __init__(self):
        # Load data from CSV files
        self.price_data = self.load_price_data()
        self.events_data = self.load_events_data()
        self.change_points_data = self.load_change_points_data()
    
    def load_price_data(self):
        """Load historical Brent oil prices"""
        try:
            # Get the project root directory (brent-oil-analysis)
            current_file = os.path.abspath(__file__)  # C:\brent-oil-analysis\dashboard\backend\data_handler.py
            backend_dir = os.path.dirname(current_file)  # C:\brent-oil-analysis\dashboard\backend
            dashboard_dir = os.path.dirname(backend_dir)  # C:\brent-oil-analysis\dashboard
            project_root = os.path.dirname(dashboard_dir)  # C:\brent-oil-analysis
            
            # Check multiple possible data locations
            possible_paths = [
                os.path.join(project_root, 'data', 'brent_oil_prices.csv'),  # C:\brent-oil-analysis\data\brent_oil_prices.csv
                os.path.join(project_root, 'data', 'processed', 'brent_oil_processed.csv'),  # C:\brent-oil-analysis\data\processed\brent_oil_processed.csv
                os.path.join(dashboard_dir, 'data', 'brent_oil_prices.csv'),  # C:\brent-oil-analysis\dashboard\data\brent_oil_prices.csv
                os.path.join(dashboard_dir, 'data', 'processed', 'brent_oil_processed.csv'),  # C:\brent-oil-analysis\dashboard\data\processed\brent_oil_processed.csv
            ]
            
            data_loaded = False
            df = None
            
            for data_path in possible_paths:
                if os.path.exists(data_path):
                    print(f"Loading price data from: {data_path}")
                    try:
                        df = pd.read_csv(data_path)
                        print(f"Successfully loaded file with shape: {df.shape}")
                        data_loaded = True
                        break
                    except Exception as e:
                        print(f"Error reading {data_path}: {e}")
                        continue
            
            if not data_loaded:
                print("No data file found in any of the checked locations. Generating sample data...")
                return self.generate_sample_price_data()
            
            # Convert date column if exists
            date_column = None
            for col in ['Date', 'date', 'DATE', 'timestamp', 'Timestamp']:
                if col in df.columns:
                    date_column = col
                    break
            
            if date_column:
                df['date'] = pd.to_datetime(df[date_column], errors='coerce')
                # Drop rows with invalid dates
                df = df.dropna(subset=['date'])
            else:
                # If no date column, create one
                print("Warning: No date column found. Creating date index...")
                df['date'] = pd.date_range(start='2010-01-01', periods=len(df), freq='D')
            
            # Ensure price column exists
            price_column = None
            for col in ['Price', 'price', 'PRICE', 'value', 'Value']:
                if col in df.columns:
                    price_column = col
                    break
            
            if price_column:
                df['price'] = pd.to_numeric(df[price_column], errors='coerce')
                # Drop rows with invalid prices
                df = df.dropna(subset=['price'])
            else:
                print("Warning: No price column found. Using sample data.")
                return self.generate_sample_price_data()
            
            # Sort by date
            df = df.sort_values('date')
            df = df.reset_index(drop=True)
            
            # Calculate log returns using pandas Series shift method
            df['log_return'] = np.log(df['price']) - np.log(df['price'].shift(1))
            df = df.dropna(subset=['log_return'])
            
            print(f"Successfully processed {len(df)} price records from {df['date'].min()} to {df['date'].max()}")
            
            # Convert to records with formatted dates
            result_df = df[['date', 'price', 'log_return']].copy()
            result_df['date'] = result_df['date'].dt.strftime('%Y-%m-%d')
            
            return result_df.to_dict('records')
            
        except Exception as e:
            print(f"Error loading price data: {e}")
            print("Generating sample price data...")
            return self.generate_sample_price_data()
    
    def generate_sample_price_data(self):
        """Generate sample price data for demonstration"""
        print("Generating sample Brent oil price data...")
        
        # Create date range from 1987 to 2022 as per the actual dataset
        dates = pd.date_range(start='1987-05-20', end='2022-09-30', freq='D')
        
        # Generate realistic price data with trends and shocks
        np.random.seed(42)
        n = len(dates)
        
        # Base price and trend
        base_price = 18.00  # Starting price around 1987
        trend = np.linspace(0, 82, n)  # Trend to reach ~$100 by 2022
        
        # Add seasonal component
        seasonal = 8 * np.sin(2 * np.pi * np.arange(n) / 365)
        
        # Add random walk component for realistic volatility
        random_walk = np.cumsum(np.random.normal(0, 0.8, n))
        
        # Add specific shocks for known events
        shocks = np.zeros(n)
        
        # Gulf War (1990-1991)
        gulf_war_idx = (dates >= '1990-08-02') & (dates < '1991-02-28')
        shocks[gulf_war_idx] = np.linspace(0, 25, sum(gulf_war_idx))
        
        # Asian Financial Crisis (1997-1998)
        asian_crisis_idx = (dates >= '1997-07-02') & (dates < '1998-12-31')
        shocks[asian_crisis_idx] = np.linspace(0, -20, sum(asian_crisis_idx))
        
        # 2008 Financial Crisis
        financial_crisis_idx = (dates >= '2008-09-15') & (dates < '2009-06-30')
        shocks[financial_crisis_idx] = np.linspace(0, -70, sum(financial_crisis_idx))
        
        # Arab Spring (2010-2012)
        arab_spring_idx = (dates >= '2010-12-17') & (dates < '2012-12-31')
        shocks[arab_spring_idx] = np.linspace(0, 30, sum(arab_spring_idx))
        
        # 2014 Oil Price Crash
        crash_idx = (dates >= '2014-06-01') & (dates < '2015-01-01')
        shocks[crash_idx] = np.linspace(0, -50, sum(crash_idx))
        
        # COVID-19 crash
        covid_idx = (dates >= '2020-03-01') & (dates < '2020-06-01')
        shocks[covid_idx] = np.linspace(0, -40, sum(covid_idx))
        
        # Russia-Ukraine war
        war_idx = (dates >= '2022-02-24') & (dates < '2022-09-30')
        shocks[war_idx] = np.linspace(0, 35, sum(war_idx))
        
        # Combine all components
        prices = base_price + trend + seasonal + random_walk + shocks
        prices = np.maximum(prices, 10)  # Ensure positive prices
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'price': prices
        })
        
        # Calculate log returns using pandas Series shift method
        df['log_return'] = np.log(df['price']) - np.log(df['price'].shift(1))
        df = df.dropna()
        
        print(f"Generated {len(df)} sample price records from {df['date'].min()} to {df['date'].max()}")
        
        # Format dates for JSON serialization
        result_df = df[['date', 'price', 'log_return']].copy()
        result_df['date'] = result_df['date'].dt.strftime('%Y-%m-%d')
        
        return result_df.to_dict('records')
    
    
    def load_events_data(self):
        """Load geopolitical and economic events"""
        events = [
            {
                "id": 1,
                "name": "Black Monday",
                "date": "1987-10-19",
                "type": "economic",
                "region": "Global",
                "description": "Stock market crash affecting oil prices"
            },
            {
                "id": 2,
                "name": "Gulf War",
                "date": "1990-08-02",
                "type": "political",
                "region": "Middle East",
                "description": "Iraq invasion of Kuwait causing oil price spike"
            },
            {
                "id": 3,
                "name": "Asian Financial Crisis",
                "date": "1997-07-02",
                "type": "economic",
                "region": "Asia",
                "description": "Currency devaluations reducing oil demand"
            },
            {
                "id": 4,
                "name": "9/11 Attacks",
                "date": "2001-09-11",
                "type": "political",
                "region": "North America",
                "description": "Terrorist attacks causing market uncertainty"
            },
            {
                "id": 5,
                "name": "Iraq War",
                "date": "2003-03-20",
                "type": "political",
                "region": "Middle East",
                "description": "US invasion of Iraq affecting supply"
            },
            {
                "id": 6,
                "name": "Global Financial Crisis",
                "date": "2008-09-15",
                "type": "economic",
                "region": "Global",
                "description": "Lehman Brothers collapse, severe demand shock"
            },
            {
                "id": 7,
                "name": "Arab Spring",
                "date": "2010-12-17",
                "type": "political",
                "region": "Middle East",
                "description": "Protests and uprisings affecting oil production"
            },
            {
                "id": 8,
                "name": "US Shale Boom",
                "date": "2011-01-01",
                "type": "economic",
                "region": "North America",
                "description": "Rapid increase in US shale oil production"
            },
            {
                "id": 9,
                "name": "2014 Oil Price Crash",
                "date": "2014-06-01",
                "type": "economic",
                "region": "Global",
                "description": "Sharp decline due to oversupply and weak demand"
            },
            {
                "id": 10,
                "name": "OPEC Production Cut",
                "date": "2016-11-30",
                "type": "policy",
                "region": "Global",
                "description": "OPEC agrees to cut production to stabilize prices"
            },
            {
                "id": 11,
                "name": "COVID-19 Pandemic",
                "date": "2020-03-11",
                "type": "economic",
                "region": "Global",
                "description": "Global pandemic causing unprecedented demand shock"
            },
            {
                "id": 12,
                "name": "Saudi-Russia Price War",
                "date": "2020-03-08",
                "type": "economic",
                "region": "Global",
                "description": "Price war between major oil producers"
            },
            {
                "id": 13,
                "name": "Russia-Ukraine War",
                "date": "2022-02-24",
                "type": "political",
                "region": "Europe",
                "description": "Conflict leading to sanctions and supply disruptions"
            }
        ]
        return events
    
    def load_change_points_data(self):
        """Load detected change points from Bayesian analysis"""
        change_points = [
            {
                "date": "1990-08-15",
                "probability": 0.92,
                "before_mean": 18.5,
                "after_mean": 28.7,
                "change_percentage": 55.1,
                "associated_events": [2]
            },
            {
                "date": "2008-09-20",
                "probability": 0.98,
                "before_mean": 115.4,
                "after_mean": 65.2,
                "change_percentage": -43.5,
                "associated_events": [6]
            },
            {
                "date": "2014-06-15",
                "probability": 0.95,
                "before_mean": 110.5,
                "after_mean": 60.3,
                "change_percentage": -45.4,
                "associated_events": [9]
            },
            {
                "date": "2016-12-01",
                "probability": 0.88,
                "before_mean": 45.2,
                "after_mean": 55.8,
                "change_percentage": 23.5,
                "associated_events": [10]
            },
            {
                "date": "2020-03-15",
                "probability": 0.99,
                "before_mean": 65.4,
                "after_mean": 30.1,
                "change_percentage": -54.0,
                "associated_events": [11, 12]
            },
            {
                "date": "2022-03-01",
                "probability": 0.93,
                "before_mean": 75.6,
                "after_mean": 105.3,
                "change_percentage": 39.3,
                "associated_events": [13]
            }
        ]
        return change_points
    
    def get_price_data(self):
        return self.price_data
    
    def filter_by_date(self, start_date, end_date):
        """Filter price data by date range"""
        try:
            df = pd.DataFrame(self.price_data)
            # Ensure date column is datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Parse input dates
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            mask = (df['date'] >= start_dt) & (df['date'] <= end_dt)
            filtered_df = df[mask].copy()
            
            # Format dates for JSON serialization
            filtered_df['date'] = filtered_df['date'].dt.strftime('%Y-%m-%d')
            
            print(f"Filtered data: {len(filtered_df)} records from {start_date} to {end_date}")
            return filtered_df.to_dict('records')
        except Exception as e:
            print(f"Error filtering by date: {e}")
            return []
    
    def get_change_points(self):
        return self.change_points_data
    
    def get_events(self):
        return self.events_data
    
    def get_event_correlation(self, event_id):
        """Get correlation analysis for specific event"""
        try:
            event_id = int(event_id)
            event = next((e for e in self.events_data if e['id'] == event_id), None)
            if not event:
                return {"error": "Event not found"}
            
            # Find corresponding change point
            change_point = next(
                (cp for cp in self.change_points_data 
                 if event_id in cp.get('associated_events', [])),
                None
            )
            
            # Calculate price impact
            price_analysis = self.calculate_event_impact(event['date'])
            
            return {
                "event": event,
                "change_point": change_point,
                "price_analysis": price_analysis
            }
        except Exception as e:
            print(f"Error getting event correlation: {e}")
            return {"error": str(e)}
    
    def calculate_volatility(self):
        """Calculate volatility metrics"""
        try:
            df = pd.DataFrame(self.price_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            returns = df['log_return'].dropna()
            
            # Calculate rolling volatility
            rolling_vol = returns.rolling(window=30).std().tolist()
            rolling_dates = df['date'].iloc[29:].dt.strftime('%Y-%m-%d').tolist()
            
            # Filter out NaN values
            rolling_data = []
            for d, v in zip(rolling_dates, rolling_vol):
                if not np.isnan(v):
                    rolling_data.append({"date": d, "volatility": float(v)})
            
            return {
                "daily_volatility": float(returns.std()),
                "annualized_volatility": float(returns.std() * np.sqrt(252)),
                "rolling_volatility": rolling_data,
                "max_drawdown": float(self.calculate_max_drawdown(df['price'].values))
            }
        except Exception as e:
            print(f"Error calculating volatility: {e}")
            return {
                "daily_volatility": 0.0,
                "annualized_volatility": 0.0,
                "rolling_volatility": [],
                "max_drawdown": 0.0
            }
    
    def calculate_max_drawdown(self, prices):
        """Calculate maximum drawdown"""
        try:
            cumulative = np.maximum.accumulate(prices)
            drawdown = (cumulative - prices) / cumulative
            return float(np.nanmax(drawdown))
        except Exception as e:
            print(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def get_summary_statistics(self):
        """Get summary statistics for the dashboard"""
        try:
            df = pd.DataFrame(self.price_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            price_stats = df['price'].describe()
            
            return {
                "total_days": len(df),
                "date_range": {
                    "start": df['date'].min().strftime('%Y-%m-%d'),
                    "end": df['date'].max().strftime('%Y-%m-%d')
                },
                "price_statistics": {
                    "mean": float(price_stats['mean']),
                    "median": float(df['price'].median()),
                    "std": float(price_stats['std']),
                    "min": float(price_stats['min']),
                    "max": float(price_stats['max']),
                    "q1": float(df['price'].quantile(0.25)),
                    "q3": float(df['price'].quantile(0.75))
                },
                "total_change_points": len(self.change_points_data),
                "total_events": len(self.events_data)
            }
        except Exception as e:
            print(f"Error calculating summary stats: {e}")
            return {
                "total_days": 0,
                "date_range": {"start": "", "end": ""},
                "price_statistics": {
                    "mean": 0.0,
                    "median": 0.0,
                    "std": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "q1": 0.0,
                    "q3": 0.0
                },
                "total_change_points": 0,
                "total_events": 0
            }
    
    def calculate_event_impact(self, event_date, window_days=30):
        """Calculate price impact around an event"""
        try:
            df = pd.DataFrame(self.price_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            event_dt = pd.to_datetime(event_date)
            
            # Get prices around event
            start_date = event_dt - timedelta(days=window_days)
            end_date = event_dt + timedelta(days=window_days)
            
            mask = (df['date'] >= start_date) & (df['date'] <= end_date)
            event_prices = df[mask].copy()
            
            if len(event_prices) == 0:
                return None
            
            # Split into pre and post event
            pre_event = event_prices[event_prices['date'] < event_dt]
            post_event = event_prices[event_prices['date'] >= event_dt]
            
            # Format price data for chart
            event_prices['date_str'] = event_prices['date'].dt.strftime('%Y-%m-%d')
            
            result = {
                "pre_event_mean": float(pre_event['price'].mean()) if len(pre_event) > 0 else None,
                "post_event_mean": float(post_event['price'].mean()) if len(post_event) > 0 else None,
                "pre_event_std": float(pre_event['price'].std()) if len(pre_event) > 0 else None,
                "post_event_std": float(post_event['price'].std()) if len(post_event) > 0 else None,
                "window_days": window_days,
                "event_date": event_date,
                "price_data": event_prices[['date_str', 'price']].rename(
                    columns={'date_str': 'date', 'price': 'price'}
                ).to_dict('records')
            }
            
            # Calculate percentage change if possible
            if result["pre_event_mean"] and result["post_event_mean"] and result["pre_event_mean"] > 0:
                result["percentage_change"] = float(
                    ((result["post_event_mean"] - result["pre_event_mean"]) / 
                     result["pre_event_mean"] * 100)
                )
            else:
                result["percentage_change"] = None
                
            return result
            
        except Exception as e:
            print(f"Error calculating event impact for {event_date}: {e}")
            return None
    
    def calculate_price_impact(self, event_date, window_days):
        """Calculate price impact (alias for calculate_event_impact)"""
        return self.calculate_event_impact(event_date, window_days)