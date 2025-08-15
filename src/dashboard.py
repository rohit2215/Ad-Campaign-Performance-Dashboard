"""
Ad Campaign Performance Dashboard

This Streamlit application creates an interactive dashboard for analyzing
ad campaign performance data. It provides visualizations, KPIs, and insights
in a user-friendly interface.

Key Features:
- Interactive KPI dashboard
- Performance visualizations
- Filtering and segmentation
- Trend analysis
- Optimization recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Ad Campaign Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 0.5rem 0;
        color: #333;
    }
    .insight-box h4 {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .insight-box p {
        color: #333;
        margin: 0.25rem 0;
    }
    .insight-box strong {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """
    Load all the processed data files.
    
    Returns:
    - Dictionary containing all dataframes
    """
    data = {}
    
    # Load main processed data
    try:
        data['main'] = pd.read_csv('data/campaign_data_processed.csv')
        data['main']['date'] = pd.to_datetime(data['main']['date'])
    except FileNotFoundError:
        st.error("❌ Processed data not found. Please run data_processing.py first.")
        return None
    
    # Load analysis results
    try:
        data['campaign_performance'] = pd.read_csv('data/campaign_performance.csv')
        data['device_performance'] = pd.read_csv('data/device_performance.csv')
        data['location_performance'] = pd.read_csv('data/location_performance.csv')
        data['daily_trends'] = pd.read_csv('data/daily_trends.csv')
        data['daily_trends']['date'] = pd.to_datetime(data['daily_trends']['date'])
    except FileNotFoundError:
        st.warning("⚠️ Analysis results not found. Please run analysis.py first.")
    
    return data

def calculate_kpis(df):
    """
    Calculate overall KPIs from the data.
    
    Parameters:
    - df: Main dataframe
    
    Returns:
    - Dictionary with KPI values
    """
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    total_conversions = df['conversions'].sum()
    total_cost = df['cost'].sum()
    total_revenue = df['revenue'].sum()
    
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
    cpa = (total_cost / total_conversions) if total_conversions > 0 else 0
    roas = (total_revenue / total_cost) if total_cost > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    
    return {
        'impressions': total_impressions,
        'clicks': total_clicks,
        'conversions': total_conversions,
        'cost': total_cost,
        'revenue': total_revenue,
        'ctr': ctr,
        'cpc': cpc,
        'cpa': cpa,
        'roas': roas,
        'conversion_rate': conversion_rate
    }

def create_kpi_cards(kpis):
    """
    Create KPI metric cards for the dashboard.
    
    Parameters:
    - kpis: Dictionary with KPI values
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-value">{kpis['ctr']:.2f}%</div>
            <div class="kpi-label">Click-Through Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-value">${kpis['cpc']:.2f}</div>
            <div class="kpi-label">Cost Per Click</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-value">${kpis['cpa']:.2f}</div>
            <div class="kpi-label">Cost Per Acquisition</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-value">{kpis['roas']:.2f}x</div>
            <div class="kpi-label">Return on Ad Spend</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-value">{kpis['conversion_rate']:.2f}%</div>
            <div class="kpi-label">Conversion Rate</div>
        </div>
        """, unsafe_allow_html=True)

def create_revenue_cost_chart(df):
    """
    Create revenue vs cost chart.
    
    Parameters:
    - df: Main dataframe
    """
    daily_data = df.groupby('date').agg({
        'revenue': 'sum',
        'cost': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_data['date'],
        y=daily_data['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_data['date'],
        y=daily_data['cost'],
        mode='lines+markers',
        name='Cost',
        line=dict(color='#d62728', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Daily Revenue vs Cost Trend',
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_campaign_performance_chart(campaign_data):
    """
    Create campaign performance comparison chart.
    
    Parameters:
    - campaign_data: Campaign performance dataframe
    """
    fig = px.bar(
        campaign_data,
        x='campaign_name',
        y=['revenue', 'cost'],
        title='Campaign Performance: Revenue vs Cost',
        barmode='group',
        color_discrete_map={'revenue': '#2ca02c', 'cost': '#d62728'}
    )
    
    fig.update_layout(
        xaxis_title='Campaign',
        yaxis_title='Amount ($)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_device_performance_chart(device_data):
    """
    Create device performance chart.
    
    Parameters:
    - device_data: Device performance dataframe
    """
    fig = px.pie(
        device_data,
        values='revenue',
        names='device',
        title='Revenue Distribution by Device',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_location_heatmap(location_data):
    """
    Create location performance heatmap.
    
    Parameters:
    - location_data: Location performance dataframe
    """
    # Create a heatmap of ROAS by location
    fig = px.bar(
        location_data.sort_values('roas', ascending=True),
        x='roas',
        y='location',
        orientation='h',
        title='ROAS by Location',
        color='roas',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_title='ROAS',
        yaxis_title='Location',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_trend_analysis(daily_data):
    """
    Create trend analysis charts.
    
    Parameters:
    - daily_data: Daily trends dataframe
    """
    # Create subplots for different metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CTR Trend', 'ROAS Trend', 'CPC Trend', 'Conversion Rate Trend'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # CTR Trend
    fig.add_trace(
        go.Scatter(x=daily_data['date'], y=daily_data['ctr'], name='CTR', line=dict(color='#1f77b4')),
        row=1, col=1
    )
    
    # ROAS Trend
    fig.add_trace(
        go.Scatter(x=daily_data['date'], y=daily_data['roas'], name='ROAS', line=dict(color='#2ca02c')),
        row=1, col=2
    )
    
    # CPC Trend
    fig.add_trace(
        go.Scatter(x=daily_data['date'], y=daily_data['cpc'], name='CPC', line=dict(color='#d62728')),
        row=2, col=1
    )
    
    # Conversion Rate Trend
    conversion_rate = (daily_data['conversions'] / daily_data['clicks'] * 100).fillna(0)
    fig.add_trace(
        go.Scatter(x=daily_data['date'], y=conversion_rate, name='Conv Rate', line=dict(color='#ff7f0e')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def create_filtered_analysis(df):
    """
    Create filtered analysis based on user selections.
    
    Parameters:
    - df: Main dataframe
    """
    st.subheader("🔍 Filtered Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_campaigns = st.multiselect(
            "Select Campaigns",
            options=df['campaign_name'].unique(),
            default=df['campaign_name'].unique()[:3]
        )
    
    with col2:
        selected_devices = st.multiselect(
            "Select Devices",
            options=df['device'].unique(),
            default=df['device'].unique()
        )
    
    with col3:
        date_range = st.date_input(
            "Select Date Range",
            value=(df['date'].min(), df['date'].max()),
            min_value=df['date'].min(),
            max_value=df['date'].max()
        )
    
    # Apply filters
    filtered_df = df[
        (df['campaign_name'].isin(selected_campaigns)) &
        (df['device'].isin(selected_devices)) &
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1]))
    ]
    
    if not filtered_df.empty:
        # Calculate filtered KPIs
        filtered_kpis = calculate_kpis(filtered_df)
        
        st.write("**Filtered Performance Summary:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Revenue", f"${filtered_kpis['revenue']:,.2f}")
        with col2:
            st.metric("Cost", f"${filtered_kpis['cost']:,.2f}")
        with col3:
            st.metric("ROAS", f"{filtered_kpis['roas']:.2f}x")
        with col4:
            st.metric("CTR", f"{filtered_kpis['ctr']:.2f}%")
        
        # Show filtered data
        st.dataframe(filtered_df.head(10))
    else:
        st.warning("No data matches the selected filters.")

def create_insights_section(data):
    """
    Create insights and recommendations section.
    
    Parameters:
    - data: Dictionary containing all dataframes
    """
    st.subheader("💡 Insights & Recommendations")
    
    if 'campaign_performance' in data:
        campaign_data = data['campaign_performance']
        
        # Top performers
        best_campaign = campaign_data.loc[campaign_data['roas'].idxmax()]
        worst_campaign = campaign_data.loc[campaign_data['roas'].idxmin()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="insight-box">
                <h4>🏆 Best Performing Campaign</h4>
                <p><strong>{best_campaign['campaign_name']}</strong></p>
                <p>ROAS: {best_campaign['roas']:.2f}x | Revenue: ${best_campaign['revenue']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if worst_campaign['roas'] < 1.0:
                st.markdown(f"""
                <div class="insight-box">
                    <h4>⚠️ Optimization Opportunity</h4>
                    <p><strong>{worst_campaign['campaign_name']}</strong></p>
                    <p>ROAS: {worst_campaign['roas']:.2f}x - Consider pausing or optimizing</p>
                </div>
                """, unsafe_allow_html=True)
    
    if 'location_performance' in data:
        location_data = data['location_performance']
        best_location = location_data.loc[location_data['roas'].idxmax()]
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>📍 Top Performing Location</h4>
            <p><strong>{best_location['location']}</strong> has the highest ROAS at {best_location['roas']:.2f}x</p>
            <p>Consider expanding budget allocation to this location.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    Main dashboard function.
    """
    # Header
    st.markdown('<h1 class="main-header">📊 Ad Campaign Performance Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a Section",
        ["📈 Overview", "🎯 Campaign Analysis", "📱 Device Analysis", "📍 Location Analysis", "📊 Trend Analysis", "🔍 Filtered Analysis"]
    )
    
    # Main content
    if page == "📈 Overview":
        st.header("📈 Campaign Performance Overview")
        
        # Calculate and display KPIs
        kpis = calculate_kpis(data['main'])
        create_kpi_cards(kpis)
        
        # Revenue vs Cost chart
        st.subheader("💰 Revenue vs Cost Trend")
        create_revenue_cost_chart(data['main'])
        
        # Insights
        create_insights_section(data)
        
    elif page == "🎯 Campaign Analysis":
        st.header("🎯 Campaign Performance Analysis")
        
        if 'campaign_performance' in data:
            create_campaign_performance_chart(data['campaign_performance'])
            
            # Campaign performance table
            st.subheader("📋 Campaign Performance Details")
            st.dataframe(data['campaign_performance'])
        else:
            st.warning("Campaign performance data not available. Please run analysis.py first.")
    
    elif page == "📱 Device Analysis":
        st.header("📱 Device Performance Analysis")
        
        if 'device_performance' in data:
            col1, col2 = st.columns(2)
            
            with col1:
                create_device_performance_chart(data['device_performance'])
            
            with col2:
                st.subheader("📊 Device Performance Summary")
                st.dataframe(data['device_performance'])
        else:
            st.warning("Device performance data not available. Please run analysis.py first.")
    
    elif page == "📍 Location Analysis":
        st.header("📍 Location Performance Analysis")
        
        if 'location_performance' in data:
            create_location_heatmap(data['location_performance'])
            
            st.subheader("📋 Location Performance Details")
            st.dataframe(data['location_performance'])
        else:
            st.warning("Location performance data not available. Please run analysis.py first.")
    
    elif page == "📊 Trend Analysis":
        st.header("📊 Performance Trends")
        
        if 'daily_trends' in data:
            create_trend_analysis(data['daily_trends'])
        else:
            st.warning("Daily trends data not available. Please run analysis.py first.")
    
    elif page == "🔍 Filtered Analysis":
        st.header("🔍 Custom Analysis")
        create_filtered_analysis(data['main'])
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Data Summary:**")
    st.sidebar.markdown(f"📅 Date Range: {data['main']['date'].min().strftime('%Y-%m-%d')} to {data['main']['date'].max().strftime('%Y-%m-%d')}")
    st.sidebar.markdown(f"🎯 Campaigns: {data['main']['campaign_id'].nunique()}")
    st.sidebar.markdown(f"📱 Devices: {data['main']['device'].nunique()}")
    st.sidebar.markdown(f"📍 Locations: {data['main']['location'].nunique()}")
    st.sidebar.markdown(f"📊 Total Records: {len(data['main']):,}")

if __name__ == "__main__":
    main() 