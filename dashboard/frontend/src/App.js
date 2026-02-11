import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check API connectivity
    fetch('http://localhost:5000/')
      .then(response => response.json())
      .then(() => setLoading(false))
      .catch(err => {
        setError('Failed to connect to backend API. Make sure Flask server is running on port 5000.');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Connection Error</h4>
          <p>{error}</p>
          <hr />
          <p className="mb-0">
            Please ensure the Flask backend is running on http://localhost:5000
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>Brent Oil Prices Analysis Dashboard</h1>
          <p className="subtitle">Interactive visualization of geopolitical events impact on oil prices</p>
        </div>
      </header>
      <main>
        <Dashboard />
      </main>
      <footer className="app-footer">
        <div className="container">
          <p>Birhan Energies &copy; 2026 | Change Point Analysis System</p>
        </div>
      </footer>
    </div>
  );
}

export default App;