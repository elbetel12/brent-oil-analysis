# Brent Oil Price Change Point Analysis Plan

## 1. Analysis Workflow

### Step 1: Data Preparation
- Load historical Brent oil prices dataset
- Clean and format date column
- Handle missing values

### Step 2: Exploratory Data Analysis (EDA)
- Visualize price trends over time
- Analyze statistical properties
- Test for stationarity (ADF test)
- Examine volatility patterns

### Step 3: Event Data Compilation
- Research major geopolitical and economic events
- Create structured events dataset with dates and descriptions

### Step 4: Change Point Modeling
- Implement Bayesian Change Point Detection using PyMC
- Identify structural breaks in price series
- Quantify parameter changes before/after breakpoints

### Step 5: Event Correlation Analysis
- Map detected change points to historical events
- Formulate causal hypotheses
- Quantify impact of key events

### Step 6: Dashboard Development
- Build interactive visualization platform
- Implement event highlighting functionality
- Enable filtering and exploration

### Step 7: Reporting and Communication
- Generate comprehensive report
- Create presentation materials
- Prepare executive summary