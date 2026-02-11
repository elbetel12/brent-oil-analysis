# Brent Oil Dashboard - Frontend

## Setup Instructions

1. Install Node.js (v14 or higher)
2. Navigate to frontend directory:
   ```bash
   cd frontend
Install dependencies:

bash
npm install
Create .env file (optional):

env
REACT_APP_API_URL=http://localhost:5000/api
Start the development server:

bash
npm start
Open http://localhost:3000 in your browser

Features
Interactive Price Charts: Visualize Brent oil price trends with event markers

Event Correlation Analysis: Explore how specific events impacted prices

Change Point Visualization: View detected structural breaks with probability metrics

Filtering System: Filter by date range, event types, and regions

Responsive Design: Works on desktop, tablet, and mobile devices

Dashboard Components
Price Analysis Tab: Main price chart with event overlays

Event Correlation Tab: Detailed event impact analysis

Change Points Tab: Bayesian change point detection results

Insights Tab: Key findings and observations

Tech Stack
React 18

Recharts for data visualization

React Bootstrap for UI components

Axios for API calls

React Datepicker for date selection