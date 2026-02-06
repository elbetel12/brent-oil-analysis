"""
Data preprocessing module for Brent oil price analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """Preprocess Brent oil price data."""
    
    def __init__(self, filepath):
        """
        Initialize preprocessor.
        
        Args:
            filepath (str): Path to raw data CSV file
        """
        self.filepath = filepath
        self.df = None
        
    def load_data(self):
        """Load and clean raw data."""
        # Load data
        self.df = pd.read_csv(self.filepath)
        
        # Convert date
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%b-%y')
        
        # Sort by date
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
        # Handle missing values
        self.df['Price'] = self.df['Price'].fillna(method='ffill')
        
        return self.df
    
    def create_features(self):
        """Create additional features for analysis."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Time-based features
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Quarter'] = self.df['Date'].dt.quarter
        self.df['DayOfWeek'] = self.df['Date'].dt.dayofweek
        
        # Returns
        self.df['Daily_Return'] = self.df['Price'].pct_change()
        self.df['Log_Return'] = np.log(self.df['Price']/self.df['Price'].shift(1))
        
        # Rolling statistics
        self.df['Rolling_Mean_30'] = self.df['Price'].rolling(window=30).mean()
        self.df['Rolling_Std_30'] = self.df['Price'].rolling(window=30).std()
        
        return self.df
    
    def filter_date_range(self, start_date=None, end_date=None):
        """Filter data by date range."""
        if start_date:
            self.df = self.df[self.df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            self.df = self.df[self.df['Date'] <= pd.to_datetime(end_date)]
        
        return self.df
    
    def save_processed_data(self, output_path):
        """Save processed data to CSV."""
        if self.df is None:
            raise ValueError("No data to save.")
        
        self.df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        
    def get_summary_stats(self):
        """Get summary statistics."""
        if self.df is None:
            raise ValueError("Data not loaded.")
        
        summary = {
            'start_date': self.df['Date'].min(),
            'end_date': self.df['Date'].max(),
            'total_days': len(self.df),
            'avg_price': self.df['Price'].mean(),
            'max_price': self.df['Price'].max(),
            'min_price': self.df['Price'].min(),
            'avg_daily_return': self.df['Daily_Return'].mean() * 100,
            'volatility': self.df['Daily_Return'].std() * 100
        }
        
        return summary


def load_events_data(filepath):
    """Load and preprocess events data."""
    events_df = pd.read_csv(filepath)
    events_df['date'] = pd.to_datetime(events_df['date'])
    return events_df


if __name__ == "__main__":
    # Example usage
    preprocessor = DataPreprocessor('../data/raw/brent_oil_prices.csv')
    df = preprocessor.load_data()
    df = preprocessor.create_features()
    
    stats = preprocessor.get_summary_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")