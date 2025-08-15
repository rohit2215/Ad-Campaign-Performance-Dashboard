# 📊 Ad Campaign Performance Dashboard - Complete Interview Guide

## 🎯 Project Overview

**What I Built:** An end-to-end advertising analytics pipeline that simulates how data analysts work with real advertising data in companies like Google, Facebook, and InMobi.

**Why This Matters:** This demonstrates the complete workflow from raw data to business insights - exactly what you'd do as a data analyst.

---

## 🏗️ Step-by-Step Technical Breakdown

### Step 1: Data Generation (`src/data_generation.py`)

**What I Did:** Created realistic synthetic advertising data that mimics real-world patterns.

**Why Synthetic Data?**
- Safe to experiment (no real company data)
- Controlled environment (we know what patterns to expect)
- Reproducible results (same every time)

**Key Technical Concepts:**

```python
def generate_campaign_data(start_date='2024-01-01', days=90):
    # Create 90 days of data
    date_range = pd.date_range(start=start_date, periods=days, freq='D')
    
    # Define 5 campaigns with different characteristics
    campaigns = [
        {'id': 'CAMP_001', 'name': 'Summer Sale 2024', 'budget': 5000, 'type': 'Search'},
        {'id': 'CAMP_002', 'name': 'Brand Awareness', 'budget': 3000, 'type': 'Display'},
        # ... more campaigns
    ]
```

**Realistic Data Relationships I Created:**
- **Search campaigns** have higher CTR (2%) than display campaigns (0.5%)
- **Mobile devices** get more traffic (50%) than desktop (40%) and tablet (10%)
- **Weekend traffic** is lower than weekday traffic
- **Cost per click** varies by campaign type and competition

**Anomaly Injection:**
```python
def add_anomalies(df, anomaly_rate=0.05):
    # Add realistic data problems
    # Missing values, outliers, data errors
```

**Why Add Problems?** Real data is messy! This teaches you how to handle:
- Missing values (NaN)
- Outliers (extreme values)
- Data errors (negative clicks)

### Step 2: Data Processing (`src/data_processing.py`)

**What I Did:** Cleaned and prepared the raw data for analysis.

**Data Quality Assessment:**
```python
def assess_data_quality(df):
    # Check for missing values
    missing_data = df.isnull().sum()
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    
    # Validate data types
    data_types = df.dtypes
```

**Data Cleaning Process:**

1. **Handle Missing Values:**
```python
# Fill missing clicks with 0 (logical default)
df_clean['clicks'] = df_clean['clicks'].fillna(0)

# Fill missing cost with median (preserves typical pattern)
median_cost = df_clean['cost'].median()
df_clean['cost'] = df_clean['cost'].fillna(median_cost)
```

2. **Remove Impossible Values:**
```python
# Remove negative clicks (impossible in advertising)
df_clean = df_clean[df_clean['clicks'] >= 0]
```

3. **Handle Outliers Using IQR Method:**
```python
Q1 = df_clean[col].quantile(0.25)  # 25th percentile
Q3 = df_clean[col].quantile(0.75)  # 75th percentile
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Cap outliers instead of removing them
df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
```

**Feature Engineering:**
```python
# Add time-based features
df_features['day_of_week'] = df_features['date'].dt.day_name()
df_features['is_weekend'] = df_features['date'].dt.weekday >= 5

# Add performance categories
df_features['ctr_category'] = pd.cut(
    df_features['ctr'], 
    bins=[0, 1, 2, 5, 100], 
    labels=['Low', 'Medium', 'High', 'Very High']
)
```

### Step 3: Analysis (`src/analysis.py`)

**What I Did:** Calculated KPIs, performed segmentation analysis, and generated insights.

**KPI Calculation:**
```python
def calculate_overall_kpis(df):
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    total_conversions = df['conversions'].sum()
    total_cost = df['cost'].sum()
    total_revenue = df['revenue'].sum()
    
    # Calculate KPIs
    ctr = (total_clicks / total_impressions * 100)
    cpc = (total_cost / total_clicks)
    cpa = (total_cost / total_conversions)
    roas = (total_revenue / total_cost)
    conversion_rate = (total_conversions / total_clicks * 100)
```

**Key KPIs Explained:**

1. **CTR (Click-Through Rate):** `clicks / impressions * 100`
   - Measures ad relevance
   - Good: 1-3% for search, 0.1-1% for display

2. **CPC (Cost Per Click):** `cost / clicks`
   - Measures advertising efficiency
   - Industry average: $1-3

3. **CPA (Cost Per Acquisition):** `cost / conversions`
   - Measures customer acquisition cost
   - Directly affects profitability

4. **ROAS (Return on Ad Spend):** `revenue / cost`
   - Primary success metric
   - Good: >4x excellent, >2x good, <1x losing money

5. **Conversion Rate:** `conversions / clicks * 100`
   - Measures website effectiveness
   - Industry average: 1-5%

**Segmentation Analysis:**
```python
# Campaign performance
campaign_performance = df.groupby(['campaign_id', 'campaign_name']).agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'cost': 'sum',
    'revenue': 'sum'
}).reset_index()

# Device performance
device_performance = df.groupby('device').agg({
    'revenue': 'sum',
    'cost': 'sum'
}).reset_index()

# Location performance
location_performance = df.groupby('location').agg({
    'roas': 'mean',
    'revenue': 'sum'
}).reset_index()
```

**Time Series Analysis:**
```python
# Daily performance trends
daily_performance = df.groupby('date').agg({
    'revenue': 'sum',
    'cost': 'sum'
}).reset_index()

# Moving averages for trend smoothing
daily_performance['revenue_ma7'] = daily_performance['revenue'].rolling(window=7).mean()
```

**Anomaly Detection:**
```python
def detect_anomalies(df, threshold=2.0):
    # Z-score method
    z_scores = np.abs((daily_metrics[metric] - mean_val) / std_val)
    anomaly_dates = daily_metrics[z_scores > threshold]['date']
```

**Z-Score Explained:**
- Measures how many standard deviations a value is from the mean
- Threshold of 2.0: Values >2 standard deviations away are anomalies
- Helps identify unusual performance that needs investigation

### Step 4: Dashboard (`src/dashboard.py`)

**What I Did:** Built an interactive web application using Streamlit and Plotly.

**Why Streamlit?**
- Python-based (easy to learn)
- Interactive widgets
- Beautiful visualizations
- Fast development

**Dashboard Structure:**

1. **Page Configuration:**
```python
st.set_page_config(
    page_title="Ad Campaign Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

2. **Data Loading with Caching:**
```python
@st.cache_data
def load_data():
    # Load once, reuse for performance
    data = {}
    data['main'] = pd.read_csv('data/campaign_data_processed.csv')
    return data
```

3. **KPI Cards:**
```python
def create_kpi_cards(kpis):
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-value">{kpis['ctr']:.2f}%</div>
            <div class="kpi-label">Click-Through Rate</div>
        </div>
        """, unsafe_allow_html=True)
```

4. **Interactive Charts:**
```python
def create_revenue_cost_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_data['date'],
        y=daily_data['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#2ca02c', width=3)
    ))
```

5. **Navigation:**
```python
page = st.sidebar.selectbox(
    "Choose a Section",
    ["📈 Overview", "🎯 Campaign Analysis", "📱 Device Analysis", "📍 Location Analysis"]
)
```

6. **Interactive Filters:**
```python
selected_campaigns = st.multiselect(
    "Select Campaigns",
    options=df['campaign_name'].unique(),
    default=df['campaign_name'].unique()[:3]
)
```

---

## 🎯 Business Context & Impact

### Why This Matters in Real Companies:

**1. Data-Driven Decisions:**
- No guessing - use data to make decisions
- A/B testing - compare different approaches
- ROI measurement - know if investments are working

**2. Budget Optimization:**
- Allocate resources to best performers
- Cut losses on poor performers
- Scale winners for maximum impact

**3. Performance Monitoring:**
- Real-time alerts for performance drops
- Trend analysis for long-term patterns
- Anomaly detection for unusual activity

**4. Stakeholder Communication:**
- Executive dashboards for leadership
- Team reports for analysts
- Client presentations with professional visuals

### Industry Standards:

**Advertising KPIs:**
- **CTR:** 1-3% (search), 0.1-1% (display)
- **CPC:** $1-3 (varies by industry)
- **ROAS:** >4x (excellent), >2x (good), <1x (problem)
- **Conversion Rate:** 1-5% (varies by industry)

---

## 🚀 How to Explain This in Interviews

### 1. Project Overview (30 seconds):
*"I built an end-to-end advertising analytics pipeline that simulates how data analysts work with real advertising data. It includes data generation, cleaning, analysis, and an interactive dashboard - exactly like what you'd see at companies like Google or Facebook."*

### 2. Technical Implementation (2-3 minutes):
*"I used Python with Pandas for data manipulation, created realistic synthetic data with proper relationships, implemented data cleaning techniques like outlier detection and missing value handling, calculated industry-standard KPIs like ROAS and CTR, and built an interactive dashboard using Streamlit and Plotly."*

### 3. Business Impact (1-2 minutes):
*"The dashboard helps identify which campaigns are performing well, which need optimization, and provides actionable recommendations. For example, it can detect campaigns with ROAS below 1.0 and suggest pausing them, or identify high-performing locations for budget expansion."*

### 4. Learning Outcomes (1 minute):
*"I learned how to work with time-series data, handle real-world data quality issues, create meaningful visualizations, and translate technical analysis into business insights. This mirrors exactly what I'd be doing as a data analyst."*

### 5. Technical Challenges (1 minute):
*"The biggest challenge was creating realistic data relationships and handling edge cases like division by zero in KPI calculations. I solved this by implementing proper data validation and using conditional logic to handle these scenarios."*

---

## 📚 Key Technical Concepts to Know

### Python Libraries:
- **Pandas:** Data manipulation and analysis
- **NumPy:** Numerical computing and arrays
- **Streamlit:** Web app framework
- **Plotly:** Interactive visualizations

### Data Structures:
- **DataFrame:** 2D table (rows and columns)
- **Series:** 1D array (single column)
- **Dictionary:** Key-value pairs

### Statistical Concepts:
- **Mean:** Average of all values
- **Median:** Middle value (robust to outliers)
- **Standard Deviation:** Measure of spread
- **Percentiles:** Divide data into parts
- **Z-Score:** How many standard deviations from mean

### Business Metrics:
- **CTR:** Click-through rate
- **CPC:** Cost per click
- **CPA:** Cost per acquisition
- **ROAS:** Return on ad spend
- **Conversion Rate:** Percentage of clicks that convert

---

## 🎯 Interview Tips

### 1. Be Specific:
- Don't just say "I built a dashboard"
- Say "I built an interactive dashboard with 6 different analysis sections, real-time filtering, and automated insights generation"

### 2. Show Business Understanding:
- Don't just talk about technical implementation
- Explain why each KPI matters and how it affects business decisions

### 3. Demonstrate Problem-Solving:
- Talk about challenges you faced and how you solved them
- Show your debugging and troubleshooting process

### 4. Highlight Learning:
- Emphasize what you learned and how you'd apply it
- Show your growth mindset and willingness to learn

### 5. Connect to Real World:
- Explain how this project relates to real business problems
- Show you understand industry context and standards

---

## 🏆 Project Success Metrics

### Technical Achievements:
- ✅ End-to-end pipeline: Data generation to insights
- ✅ Interactive dashboard: Professional user interface
- ✅ Data quality: Robust cleaning and validation
- ✅ Performance: Fast loading and responsive design
- ✅ Documentation: Comprehensive guides and comments

### Business Value:
- ✅ Actionable insights: Clear recommendations for optimization
- ✅ KPI tracking: Industry-standard metrics
- ✅ Segmentation: Multi-dimensional analysis
- ✅ Trend analysis: Time-based performance patterns
- ✅ Anomaly detection: Automated problem identification

### Learning Outcomes:
- ✅ Technical skills: Python, Pandas, Streamlit, Plotly
- ✅ Analytical thinking: Data interpretation and insights
- ✅ Business acumen: Understanding advertising metrics
- ✅ Project management: End-to-end development
- ✅ Communication: Clear documentation and presentation

---

## 💡 Key Takeaways for Interviews

### Technical Skills Demonstrated:
- Python programming and data manipulation
- Data cleaning and preprocessing
- Statistical analysis and KPI calculation
- Data visualization and dashboard development
- Web development with Streamlit

### Business Skills Demonstrated:
- Understanding of advertising metrics and KPIs
- Problem-solving and data quality management
- Communication of technical analysis to business stakeholders
- Project management and end-to-end development
- Documentation and user experience design

### Soft Skills Demonstrated:
- Attention to detail in data validation
- User experience design for intuitive interfaces
- Comprehensive documentation and setup guides
- Best practices in code organization and version control

This project demonstrates a complete understanding of the data analytics workflow and positions you as someone who can immediately contribute to data analytics teams. 