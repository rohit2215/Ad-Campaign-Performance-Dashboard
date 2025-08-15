# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/rohit2215/Ad-Campaign-Performance-Dashboard.git
cd Ad-Campaign-Performance-Dashboard
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Sample Data
```bash
python src/data_generation.py
```

### 5. Process the Data
```bash
python src/data_processing.py
```

### 6. Run Analysis
```bash
python src/analysis.py
```

### 7. Launch Dashboard
```bash
streamlit run src/dashboard.py
```

## 🎯 What You'll Get

- **Interactive Dashboard**: Beautiful visualizations of campaign performance
- **KPI Tracking**: CTR, CPC, CPA, ROAS, Conversion Rate
- **Segmentation Analysis**: By campaign, device, location
- **Trend Analysis**: Time series charts and insights
- **Optimization Recommendations**: Data-driven suggestions

## 📊 Dashboard Features

- **Overview**: Key performance indicators and trends
- **Campaign Analysis**: Performance comparison across campaigns
- **Device Analysis**: Mobile, desktop, and tablet performance
- **Location Analysis**: Geographic performance insights
- **Trend Analysis**: Time-based performance patterns
- **Filtered Analysis**: Custom data exploration

## 🛠️ Troubleshooting

### Common Issues:

1. **Port already in use**: Change the port in Streamlit
   ```bash
   streamlit run src/dashboard.py --server.port 8502
   ```

2. **Missing dependencies**: Reinstall requirements
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Data not loading**: Ensure you've run all scripts in order
   ```bash
   python src/data_generation.py
   python src/data_processing.py
   python src/analysis.py
   ```

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## 📄 License

This project is open source and available under the MIT License. 