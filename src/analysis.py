"""
Ad Campaign Analysis Engine

This script performs comprehensive analysis on the cleaned campaign data to generate
insights and recommendations. It demonstrates real-world analytical techniques used
by data analysts in advertising.

Key Concepts You'll Learn:
- KPI calculation and aggregation
- Segmentation analysis
- Time series trend analysis
- Performance comparison and benchmarking
- Anomaly detection
- Statistical analysis for insights
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_processed_data(filepath='data/campaign_data_processed.csv'):
    """
    Load the processed campaign data.
    
    Parameters:
    - filepath: Path to the processed CSV file
    
    Returns:
    - DataFrame with processed campaign data
    """
    
    print("📂 Loading processed campaign data...")
    
    try:
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        print(f"✅ Successfully loaded {len(df):,} records")
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        print("💡 Please run data_processing.py first to create the processed data")
        return None

def calculate_overall_kpis(df):
    """
    Calculate overall KPIs for the entire dataset.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - Dictionary with overall KPIs
    """
    
    print("\n📊 Calculating Overall KPIs...")
    print("=" * 50)
    
    # Aggregate metrics
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    total_conversions = df['conversions'].sum()
    total_cost = df['cost'].sum()
    total_revenue = df['revenue'].sum()
    
    # Calculate KPIs
    overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    overall_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
    overall_cpa = (total_cost / total_conversions) if total_conversions > 0 else 0
    overall_roas = (total_revenue / total_cost) if total_cost > 0 else 0
    overall_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    
    kpis = {
        'total_impressions': total_impressions,
        'total_clicks': total_clicks,
        'total_conversions': total_conversions,
        'total_cost': total_cost,
        'total_revenue': total_revenue,
        'ctr': overall_ctr,
        'cpc': overall_cpc,
        'cpa': overall_cpa,
        'roas': overall_roas,
        'conversion_rate': overall_conversion_rate
    }
    
    # Print results
    print(f"📈 Overall Performance:")
    print(f"   Impressions: {total_impressions:,}")
    print(f"   Clicks: {total_clicks:,}")
    print(f"   Conversions: {total_conversions:,}")
    print(f"   Cost: ${total_cost:,.2f}")
    print(f"   Revenue: ${total_revenue:,.2f}")
    print(f"\n🎯 Key Performance Indicators:")
    print(f"   CTR: {overall_ctr:.2f}%")
    print(f"   CPC: ${overall_cpc:.2f}")
    print(f"   CPA: ${overall_cpa:.2f}")
    print(f"   ROAS: {overall_roas:.2f}x")
    print(f"   Conversion Rate: {overall_conversion_rate:.2f}%")
    
    return kpis

def analyze_campaign_performance(df):
    """
    Analyze performance by campaign.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - DataFrame with campaign performance summary
    """
    
    print("\n🎯 Campaign Performance Analysis...")
    print("=" * 50)
    
    # Group by campaign and calculate metrics
    campaign_performance = df.groupby(['campaign_id', 'campaign_name', 'campaign_type']).agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # Calculate KPIs
    campaign_performance['ctr'] = (campaign_performance['clicks'] / campaign_performance['impressions'] * 100).round(2)
    campaign_performance['cpc'] = (campaign_performance['cost'] / campaign_performance['clicks']).round(2)
    campaign_performance['cpa'] = (campaign_performance['cost'] / campaign_performance['conversions']).round(2)
    campaign_performance['roas'] = (campaign_performance['revenue'] / campaign_performance['cost']).round(2)
    campaign_performance['conversion_rate'] = (campaign_performance['conversions'] / campaign_performance['clicks'] * 100).round(2)
    
    # Handle division by zero
    campaign_performance = campaign_performance.replace([np.inf, -np.inf], 0)
    
    # Sort by revenue
    campaign_performance = campaign_performance.sort_values('revenue', ascending=False)
    
    # Print results
    print("🏆 Top Performing Campaigns by Revenue:")
    for _, row in campaign_performance.head(3).iterrows():
        print(f"\n   {row['campaign_name']} ({row['campaign_type']})")
        print(f"   Revenue: ${row['revenue']:,.2f} | Cost: ${row['cost']:,.2f} | ROAS: {row['roas']:.2f}x")
        print(f"   CTR: {row['ctr']:.2f}% | CPC: ${row['cpc']:.2f} | Conversions: {row['conversions']:,}")
    
    return campaign_performance

def analyze_device_performance(df):
    """
    Analyze performance by device type.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - DataFrame with device performance summary
    """
    
    print("\n📱 Device Performance Analysis...")
    print("=" * 50)
    
    # Group by device and calculate metrics
    device_performance = df.groupby('device').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # Calculate KPIs
    device_performance['ctr'] = (device_performance['clicks'] / device_performance['impressions'] * 100).round(2)
    device_performance['cpc'] = (device_performance['cost'] / device_performance['clicks']).round(2)
    device_performance['cpa'] = (device_performance['cost'] / device_performance['conversions']).round(2)
    device_performance['roas'] = (device_performance['revenue'] / device_performance['cost']).round(2)
    device_performance['conversion_rate'] = (device_performance['conversions'] / device_performance['clicks'] * 100).round(2)
    
    # Handle division by zero
    device_performance = device_performance.replace([np.inf, -np.inf], 0)
    
    # Sort by revenue
    device_performance = device_performance.sort_values('revenue', ascending=False)
    
    # Print results
    print("📱 Device Performance Summary:")
    for _, row in device_performance.iterrows():
        print(f"\n   {row['device']}")
        print(f"   Revenue: ${row['revenue']:,.2f} | Cost: ${row['cost']:,.2f} | ROAS: {row['roas']:.2f}x")
        print(f"   CTR: {row['ctr']:.2f}% | CPC: ${row['cpc']:.2f} | Conversions: {row['conversions']:,}")
    
    return device_performance

def analyze_location_performance(df):
    """
    Analyze performance by location.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - DataFrame with location performance summary
    """
    
    print("\n📍 Location Performance Analysis...")
    print("=" * 50)
    
    # Group by location and calculate metrics
    location_performance = df.groupby('location').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # Calculate KPIs
    location_performance['ctr'] = (location_performance['clicks'] / location_performance['impressions'] * 100).round(2)
    location_performance['cpc'] = (location_performance['cost'] / location_performance['clicks']).round(2)
    location_performance['cpa'] = (location_performance['cost'] / location_performance['conversions']).round(2)
    location_performance['roas'] = (location_performance['revenue'] / location_performance['cost']).round(2)
    location_performance['conversion_rate'] = (location_performance['conversions'] / location_performance['clicks'] * 100).round(2)
    
    # Handle division by zero
    location_performance = location_performance.replace([np.inf, -np.inf], 0)
    
    # Sort by revenue
    location_performance = location_performance.sort_values('revenue', ascending=False)
    
    # Print results
    print("🏆 Top 5 Locations by Revenue:")
    for _, row in location_performance.head(5).iterrows():
        print(f"\n   {row['location']}")
        print(f"   Revenue: ${row['revenue']:,.2f} | Cost: ${row['cost']:,.2f} | ROAS: {row['roas']:.2f}x")
        print(f"   CTR: {row['ctr']:.2f}% | CPC: ${row['cpc']:.2f} | Conversions: {row['conversions']:,}")
    
    return location_performance

def analyze_time_trends(df):
    """
    Analyze performance trends over time.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - DataFrame with daily performance trends
    """
    
    print("\n📈 Time Series Trend Analysis...")
    print("=" * 50)
    
    # Group by date and calculate daily metrics
    daily_performance = df.groupby('date').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # Calculate daily KPIs
    daily_performance['ctr'] = (daily_performance['clicks'] / daily_performance['impressions'] * 100).round(2)
    daily_performance['cpc'] = (daily_performance['cost'] / daily_performance['clicks']).round(2)
    daily_performance['roas'] = (daily_performance['revenue'] / daily_performance['cost']).round(2)
    
    # Handle division by zero
    daily_performance = daily_performance.replace([np.inf, -np.inf], 0)
    
    # Calculate moving averages for trend analysis
    daily_performance['revenue_ma7'] = daily_performance['revenue'].rolling(window=7).mean()
    daily_performance['ctr_ma7'] = daily_performance['ctr'].rolling(window=7).mean()
    daily_performance['roas_ma7'] = daily_performance['roas'].rolling(window=7).mean()
    
    # Print trend summary
    print("📊 Performance Trends:")
    
    # Compare first and last week
    first_week = daily_performance.head(7)
    last_week = daily_performance.tail(7)
    
    first_week_avg_revenue = first_week['revenue'].mean()
    last_week_avg_revenue = last_week['revenue'].mean()
    revenue_change = ((last_week_avg_revenue - first_week_avg_revenue) / first_week_avg_revenue * 100) if first_week_avg_revenue > 0 else 0
    
    print(f"   Revenue Trend: ${first_week_avg_revenue:.2f} → ${last_week_avg_revenue:.2f} ({revenue_change:+.1f}%)")
    
    # Best and worst performing days
    best_day = daily_performance.loc[daily_performance['revenue'].idxmax()]
    worst_day = daily_performance.loc[daily_performance['revenue'].idxmin()]
    
    print(f"   Best Day: {best_day['date'].strftime('%Y-%m-%d')} (${best_day['revenue']:.2f})")
    print(f"   Worst Day: {worst_day['date'].strftime('%Y-%m-%d')} (${worst_day['revenue']:.2f})")
    
    return daily_performance

def detect_anomalies(df, threshold=2.0):
    """
    Detect anomalies in performance metrics.
    
    Parameters:
    - df: Input DataFrame
    - threshold: Standard deviation threshold for anomaly detection
    
    Returns:
    - DataFrame with detected anomalies
    """
    
    print("\n🔍 Anomaly Detection...")
    print("=" * 50)
    
    # Calculate daily performance for anomaly detection
    daily_metrics = df.groupby('date').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # Calculate KPIs
    daily_metrics['ctr'] = (daily_metrics['clicks'] / daily_metrics['impressions'] * 100)
    daily_metrics['roas'] = (daily_metrics['revenue'] / daily_metrics['cost'])
    
    # Handle division by zero
    daily_metrics = daily_metrics.replace([np.inf, -np.inf], 0)
    
    # Detect anomalies using z-score method
    anomalies = []
    
    for metric in ['impressions', 'clicks', 'revenue', 'ctr', 'roas']:
        if metric in daily_metrics.columns:
            mean_val = daily_metrics[metric].mean()
            std_val = daily_metrics[metric].std()
            
            if std_val > 0:  # Avoid division by zero
                z_scores = np.abs((daily_metrics[metric] - mean_val) / std_val)
                anomaly_dates = daily_metrics[z_scores > threshold]['date']
                
                for date in anomaly_dates:
                    value = daily_metrics[daily_metrics['date'] == date][metric].iloc[0]
                    anomalies.append({
                        'date': date,
                        'metric': metric,
                        'value': value,
                        'z_score': z_scores[daily_metrics['date'] == date].iloc[0],
                        'expected_range': f"{mean_val - threshold*std_val:.2f} - {mean_val + threshold*std_val:.2f}"
                    })
    
    if anomalies:
        print(f"⚠️ Found {len(anomalies)} anomalies:")
        for anomaly in anomalies[:5]:  # Show first 5
            print(f"   {anomaly['date'].strftime('%Y-%m-%d')}: {anomaly['metric']} = {anomaly['value']:.2f} (z-score: {anomaly['z_score']:.2f})")
    else:
        print("✅ No significant anomalies detected")
    
    return pd.DataFrame(anomalies)

def generate_insights(df, campaign_performance, device_performance, location_performance, daily_performance):
    """
    Generate actionable insights from the analysis.
    
    Parameters:
    - df: Input DataFrame
    - campaign_performance: Campaign performance summary
    - device_performance: Device performance summary
    - location_performance: Location performance summary
    - daily_performance: Daily performance trends
    
    Returns:
    - Dictionary with insights and recommendations
    """
    
    print("\n💡 Generating Insights and Recommendations...")
    print("=" * 50)
    
    insights = {
        'top_performers': [],
        'optimization_opportunities': [],
        'trends': [],
        'recommendations': []
    }
    
    # 1. Top Performers
    print("🏆 Top Performers:")
    
    # Best campaign
    best_campaign = campaign_performance.loc[campaign_performance['roas'].idxmax()]
    insights['top_performers'].append(f"Best ROAS Campaign: {best_campaign['campaign_name']} ({best_campaign['roas']:.2f}x)")
    print(f"   Best ROAS: {best_campaign['campaign_name']} ({best_campaign['roas']:.2f}x)")
    
    # Best device
    best_device = device_performance.loc[device_performance['roas'].idxmax()]
    insights['top_performers'].append(f"Best Device: {best_device['device']} (ROAS: {best_device['roas']:.2f}x)")
    print(f"   Best Device: {best_device['device']} (ROAS: {best_device['roas']:.2f}x)")
    
    # Best location
    best_location = location_performance.loc[location_performance['roas'].idxmax()]
    insights['top_performers'].append(f"Best Location: {best_location['location']} (ROAS: {best_location['roas']:.2f}x)")
    print(f"   Best Location: {best_location['location']} (ROAS: {best_location['roas']:.2f}x)")
    
    # 2. Optimization Opportunities
    print("\n🎯 Optimization Opportunities:")
    
    # Worst performing campaign
    worst_campaign = campaign_performance.loc[campaign_performance['roas'].idxmin()]
    if worst_campaign['roas'] < 1.0:
        insights['optimization_opportunities'].append(f"Consider pausing {worst_campaign['campaign_name']} (ROAS: {worst_campaign['roas']:.2f}x)")
        print(f"   Consider pausing: {worst_campaign['campaign_name']} (ROAS: {worst_campaign['roas']:.2f}x)")
    
    # High CPC campaigns
    high_cpc_campaigns = campaign_performance[campaign_performance['cpc'] > campaign_performance['cpc'].mean() * 1.5]
    for _, campaign in high_cpc_campaigns.iterrows():
        insights['optimization_opportunities'].append(f"Optimize bids for {campaign['campaign_name']} (CPC: ${campaign['cpc']:.2f})")
        print(f"   Optimize bids: {campaign['campaign_name']} (CPC: ${campaign['cpc']:.2f})")
    
    # 3. Trends
    print("\n📈 Key Trends:")
    
    # Revenue trend
    first_week_revenue = daily_performance.head(7)['revenue'].mean()
    last_week_revenue = daily_performance.tail(7)['revenue'].mean()
    revenue_trend = "increasing" if last_week_revenue > first_week_revenue else "decreasing"
    insights['trends'].append(f"Revenue trend is {revenue_trend}")
    print(f"   Revenue trend is {revenue_trend}")
    
    # Device trend
    mobile_performance = device_performance[device_performance['device'] == 'Mobile']
    if not mobile_performance.empty:
        mobile_roas = mobile_performance.iloc[0]['roas']
        insights['trends'].append(f"Mobile ROAS: {mobile_roas:.2f}x")
        print(f"   Mobile ROAS: {mobile_roas:.2f}x")
    
    # 4. Recommendations
    print("\n💡 Recommendations:")
    
    # Budget reallocation
    total_cost = campaign_performance['cost'].sum()
    high_roas_campaigns = campaign_performance[campaign_performance['roas'] > 1.5]
    if not high_roas_campaigns.empty:
        insights['recommendations'].append("Increase budget allocation to high-ROAS campaigns")
        print("   Increase budget allocation to high-ROAS campaigns")
    
    # Device optimization
    if device_performance['roas'].max() > device_performance['roas'].min() * 1.5:
        insights['recommendations'].append("Optimize device targeting based on performance")
        print("   Optimize device targeting based on performance")
    
    # Location expansion
    top_locations = location_performance.head(3)
    insights['recommendations'].append(f"Consider expanding to top-performing locations: {', '.join(top_locations['location'].tolist())}")
    print(f"   Consider expanding to top-performing locations: {', '.join(top_locations['location'].tolist())}")
    
    return insights

def save_analysis_results(campaign_performance, device_performance, location_performance, 
                         daily_performance, insights, filename='analysis_results.csv'):
    """
    Save analysis results to CSV files.
    
    Parameters:
    - Various performance DataFrames and insights
    - filename: Base filename for saving results
    """
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save campaign performance
    campaign_file = os.path.join('data', 'campaign_performance.csv')
    campaign_performance.to_csv(campaign_file, index=False)
    
    # Save device performance
    device_file = os.path.join('data', 'device_performance.csv')
    device_performance.to_csv(device_file, index=False)
    
    # Save location performance
    location_file = os.path.join('data', 'location_performance.csv')
    location_performance.to_csv(location_file, index=False)
    
    # Save daily trends
    daily_file = os.path.join('data', 'daily_trends.csv')
    daily_performance.to_csv(daily_file, index=False)
    
    print(f"\n💾 Analysis results saved:")
    print(f"   - {campaign_file}")
    print(f"   - {device_file}")
    print(f"   - {location_file}")
    print(f"   - {daily_file}")

if __name__ == "__main__":
    """
    Main execution block - this runs when you execute the script directly.
    """
    
    print("🚀 Starting Ad Campaign Analysis")
    print("=" * 50)
    
    # Load processed data
    df = load_processed_data()
    if df is None:
        exit(1)
    
    # Perform comprehensive analysis
    overall_kpis = calculate_overall_kpis(df)
    campaign_performance = analyze_campaign_performance(df)
    device_performance = analyze_device_performance(df)
    location_performance = analyze_location_performance(df)
    daily_performance = analyze_time_trends(df)
    anomalies = detect_anomalies(df)
    insights = generate_insights(df, campaign_performance, device_performance, 
                               location_performance, daily_performance)
    
    # Save results
    save_analysis_results(campaign_performance, device_performance, location_performance,
                         daily_performance, insights)
    
    print("\n🎉 Analysis complete!")
    print("💡 Next step: Run dashboard.py to view the interactive dashboard") 