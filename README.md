# Brent Oil Price Change Point Analysis

## Project Overview
Analysis of how geopolitical and economic events affect Brent oil prices using Bayesian change point detection.

## Business Context
**Birhan Energies** - Energy sector consultancy firm analyzing oil price impacts for investors, policymakers, and energy companies.

## Objectives
1. Identify key events impacting Brent oil prices over past decade
2. Quantify event impacts using statistical methods
3. Provide data-driven insights for investment and policy decisions

## Dataset
- **Source**: Historical Brent oil prices (May 20, 1987 - September 30, 2022)
- **Frequency**: Daily
- **Fields**: Date, Price (USD/barrel)

## Project Structure
brent-oil-analysis/
├── data/ # Raw and processed data
├── notebooks/ # Jupyter notebooks for analysis
├── src/ # Python source code
├── docs/ # Documentation
├── dashboard/ # Interactive dashboard
└── reports/ # Generated reports

text

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repository-url>
cd brent-oil-analysis
2. Create Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Download Dataset
Place brent_oil_prices.csv in data/raw/

5. Run EDA
bash
jupyter notebook notebooks/01_eda.ipynb
Task Progress
Task 1: Foundation (Due: Interim Submission)
Project structure setup

Analysis workflow definition

Key events compilation (15+ events)

Assumptions and limitations documented

Initial EDA completed

Task 2: Change Point Modeling
Bayesian change point detection

Event correlation analysis

Impact quantification

Task 3: Dashboard Development
Flask backend API

React frontend

Interactive visualizations