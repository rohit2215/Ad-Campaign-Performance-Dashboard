# Ad Campaign Performance Optimization Dashboard

## 🎯 Project Overview

This project simulates a real-world advertising analytics workflow, helping you understand how data analysts work with ad campaign data to provide insights and optimization recommendations.

## 📊 What You'll Learn

- **Data Generation**: Creating realistic synthetic advertising data
- **Data Cleaning**: Handling missing values, outliers, and data quality issues
- **KPI Calculation**: Computing key performance indicators (CTR, CPC, CPA, ROAS)
- **Exploratory Data Analysis**: Finding patterns and insights in campaign data
- **Dashboard Development**: Building interactive visualizations
- **Optimization Recommendations**: Automated suggestions for campaign improvement

## 🏗️ Project Structure

```
├── data/                   # Data files (raw and processed)
├── src/                    # Source code
│   ├── data_generation.py  # Generate synthetic ad campaign data
│   ├── data_processing.py  # Clean and transform data
│   ├── analysis.py         # Calculate KPIs and insights
│   ├── recommendations.py  # Generate optimization suggestions
│   └── dashboard.py        # Streamlit dashboard application
├── notebooks/              # Jupyter notebooks for exploration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Sample Data**:
   ```bash
   python src/data_generation.py
   ```

3. **Run the Dashboard**:
   ```bash
   streamlit run src/dashboard.py
   ```

## 📈 Key Features

### KPI Tracking
- **CTR (Click-Through Rate)**: Clicks / Impressions
- **CPC (Cost Per Click)**: Cost / Clicks
- **CPA (Cost Per Acquisition)**: Cost / Conversions
- **ROAS (Return on Ad Spend)**: Revenue / Cost
- **Conversion Rate**: Conversions / Clicks

### Analysis Capabilities
- Performance comparison across devices, locations, and campaigns
- Time series trend analysis
- Anomaly detection for sudden performance drops
- Budget optimization recommendations
- A/B testing simulation

### Dashboard Features
- Interactive filters for date ranges, campaigns, and devices
- Real-time KPI calculations
- Trend visualization with line charts
- Performance heatmaps
- Optimization recommendations

## 🎓 Learning Objectives

By the end of this project, you'll understand:
- How to work with time-series advertising data
- Best practices for data cleaning and validation
- How to calculate and interpret advertising KPIs
- How to build interactive dashboards
- How to provide actionable business insights

## 📚 Next Steps

After completing this project, you can extend it by:
- Adding more data sources (Google Ads, Facebook Ads)
- Implementing machine learning for predictive analytics
- Creating automated reporting systems
- Building more sophisticated optimization algorithms

---

**Happy Learning! 🎉** 