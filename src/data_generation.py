"""
Ad Campaign Data Generator

This script creates realistic synthetic advertising campaign data that mimics
real-world Microsoft Advertising or Google Ads data. It generates data with
proper relationships between metrics and realistic distributions.

Key Concepts You'll Learn:
- How to create realistic synthetic data
- Understanding advertising metrics relationships
- Time series data generation
- Handling categorical variables
- Creating derived metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_campaign_data(start_date='2024-01-01', days=90):
    """
    Generate synthetic ad campaign data for the specified date range.
    
    Parameters:
    - start_date: Start date for the data
    - days: Number of days to generate data for
    
    Returns:
    - DataFrame with campaign performance data
    """
    
    print("🎯 Generating synthetic ad campaign data...")
    print(f"📅 Date range: {start_date} to {start_date} + {days} days")
    
    # Create date range
    date_range = pd.date_range(start=start_date, periods=days, freq='D')
    
    # Define campaign configurations
    campaigns = [
        {'id': 'CAMP_001', 'name': 'Summer Sale 2024', 'budget': 5000, 'type': 'Search'},
        {'id': 'CAMP_002', 'name': 'Brand Awareness', 'budget': 3000, 'type': 'Display'},
        {'id': 'CAMP_003', 'name': 'Product Launch', 'budget': 8000, 'type': 'Search'},
        {'id': 'CAMP_004', 'name': 'Retargeting', 'budget': 2000, 'type': 'Display'},
        {'id': 'CAMP_005', 'name': 'Holiday Special', 'budget': 6000, 'type': 'Search'}
    ]
    
    # Define keywords for search campaigns
    keywords = [
        'summer sale', 'discount', 'clearance', 'brand name', 'product category',
        'best price', 'free shipping', 'limited time', 'exclusive offer', 'new arrival'
    ]
    
    # Define devices and locations
    devices = ['Desktop', 'Mobile', 'Tablet']
    locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    # Initialize empty lists to store data
    data = []
    
    # Generate data for each date
    for date in date_range:
        # Add some weekend/weekday variation
        is_weekend = date.weekday() >= 5
        
        for campaign in campaigns:
            # Generate multiple records per campaign per day (different keywords/devices)
            num_records = np.random.randint(3, 8) if not is_weekend else np.random.randint(1, 4)
            
            for _ in range(num_records):
                # Base metrics with realistic relationships
                impressions = np.random.poisson(1000 if not is_weekend else 600)
                
                # CTR varies by campaign type and device
                base_ctr = 0.02 if campaign['type'] == 'Search' else 0.005
                ctr_variation = np.random.normal(0, 0.005)
                ctr = max(0.001, min(0.1, base_ctr + ctr_variation))
                
                clicks = int(impressions * ctr)
                
                # Conversion rate depends on campaign type and CTR
                base_cvr = 0.05 if campaign['type'] == 'Search' else 0.02
                cvr_variation = np.random.normal(0, 0.01)
                conversion_rate = max(0.001, min(0.2, base_cvr + cvr_variation))
                
                conversions = int(clicks * conversion_rate)
                
                # Cost per click varies by competition and quality
                base_cpc = 2.5 if campaign['type'] == 'Search' else 0.8
                cpc_variation = np.random.normal(0, 0.5)
                cpc = max(0.1, base_cpc + cpc_variation)
                
                cost = clicks * cpc
                
                # Revenue per conversion (simplified)
                base_revenue = 50 if campaign['type'] == 'Search' else 30
                revenue_variation = np.random.normal(0, 10)
                revenue_per_conversion = max(5, base_revenue + revenue_variation)
                
                revenue = conversions * revenue_per_conversion
                
                # Select random attributes
                device = np.random.choice(devices, p=[0.4, 0.5, 0.1])  # Mobile is most common
                location = np.random.choice(locations)
                keyword = np.random.choice(keywords) if campaign['type'] == 'Search' else 'display_ad'
                
                # Create record
                record = {
                    'date': date,
                    'campaign_id': campaign['id'],
                    'campaign_name': campaign['name'],
                    'campaign_type': campaign['type'],
                    'keyword': keyword,
                    'device': device,
                    'location': location,
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'cost': round(cost, 2),
                    'revenue': round(revenue, 2)
                }
                
                data.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add derived metrics
    df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
    df['cpc'] = (df['cost'] / df['clicks']).round(2)
    df['cpa'] = (df['cost'] / df['conversions']).round(2)
    df['roas'] = (df['revenue'] / df['cost']).round(2)
    df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
    
    # Handle division by zero
    df['cpc'] = df['cpc'].replace([np.inf, -np.inf], 0)
    df['cpa'] = df['cpa'].replace([np.inf, -np.inf], 0)
    df['roas'] = df['roas'].replace([np.inf, -np.inf], 0)
    
    print(f"✅ Generated {len(df)} records across {len(campaigns)} campaigns")
    print(f"📊 Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df

def add_anomalies(df, anomaly_rate=0.05):
    """
    Add realistic anomalies to the data to simulate real-world issues.
    
    Parameters:
    - df: Input DataFrame
    - anomaly_rate: Percentage of records to modify with anomalies
    
    Returns:
    - DataFrame with anomalies added
    """
    
    print("🔍 Adding realistic anomalies to simulate real-world data...")
    
    # Create a copy to avoid modifying original
    df_anomaly = df.copy()
    
    # Select random records to add anomalies
    anomaly_indices = np.random.choice(df.index, size=int(len(df) * anomaly_rate), replace=False)
    
    for idx in anomaly_indices:
        anomaly_type = np.random.choice(['missing_data', 'outlier', 'data_error'])
        
        if anomaly_type == 'missing_data':
            # Randomly set some values to NaN
            field = np.random.choice(['clicks', 'conversions', 'cost'])
            df_anomaly.loc[idx, field] = np.nan
            
        elif anomaly_type == 'outlier':
            # Create extreme values
            field = np.random.choice(['impressions', 'clicks', 'cost'])
            if field == 'impressions':
                df_anomaly.loc[idx, field] = np.random.randint(10000, 50000)
            elif field == 'clicks':
                df_anomaly.loc[idx, field] = np.random.randint(500, 2000)
            else:  # cost
                df_anomaly.loc[idx, field] = np.random.uniform(1000, 5000)
                
        elif anomaly_type == 'data_error':
            # Create impossible values (negative clicks, etc.)
            field = np.random.choice(['clicks', 'conversions'])
            df_anomaly.loc[idx, field] = -1
    
    print(f"⚠️ Added anomalies to {len(anomaly_indices)} records")
    return df_anomaly

def save_data(df, filename='campaign_data.csv'):
    """
    Save the generated data to a CSV file.
    
    Parameters:
    - df: DataFrame to save
    - filename: Output filename
    """
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    filepath = os.path.join('data', filename)
    df.to_csv(filepath, index=False)
    
    print(f"💾 Data saved to {filepath}")
    print(f"📁 File size: {os.path.getsize(filepath) / 1024:.1f} KB")
    
    return filepath

def generate_summary_stats(df):
    """
    Generate and display summary statistics for the generated data.
    
    Parameters:
    - df: Input DataFrame
    """
    
    print("\n📈 Data Summary Statistics:")
    print("=" * 50)
    
    # Basic info
    print(f"Total records: {len(df):,}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Campaigns: {df['campaign_id'].nunique()}")
    print(f"Devices: {df['device'].nunique()}")
    print(f"Locations: {df['location'].nunique()}")
    
    # KPI averages
    print(f"\nAverage KPIs:")
    print(f"CTR: {df['ctr'].mean():.2f}%")
    print(f"CPC: ${df['cpc'].mean():.2f}")
    print(f"CPA: ${df['cpa'].mean():.2f}")
    print(f"ROAS: {df['roas'].mean():.2f}x")
    print(f"Conversion Rate: {df['conversion_rate'].mean():.2f}%")
    
    # Total metrics
    print(f"\nTotal Metrics:")
    print(f"Impressions: {df['impressions'].sum():,}")
    print(f"Clicks: {df['clicks'].sum():,}")
    print(f"Conversions: {df['conversions'].sum():,}")
    print(f"Cost: ${df['cost'].sum():,.2f}")
    print(f"Revenue: ${df['revenue'].sum():,.2f}")

if __name__ == "__main__":
    """
    Main execution block - this runs when you execute the script directly.
    """
    
    print("🚀 Starting Ad Campaign Data Generation")
    print("=" * 50)
    
    # Generate clean data
    df_clean = generate_campaign_data()
    
    # Add anomalies
    df_with_anomalies = add_anomalies(df_clean)
    
    # Save both versions
    clean_file = save_data(df_clean, 'campaign_data_clean.csv')
    anomaly_file = save_data(df_with_anomalies, 'campaign_data_with_anomalies.csv')
    
    # Generate summary statistics
    generate_summary_stats(df_clean)
    
    print("\n🎉 Data generation complete!")
    print("📁 Files created:")
    print(f"   - {clean_file} (clean data)")
    print(f"   - {anomaly_file} (data with anomalies)")
    
    print("\n💡 Next steps:")
    print("   1. Run data_processing.py to clean the data")
    print("   2. Run analysis.py to calculate insights")
    print("   3. Run dashboard.py to view the interactive dashboard") 