"""
Ad Campaign Data Processing

This script handles data cleaning and preprocessing for the ad campaign data.
It demonstrates real-world data cleaning techniques that analysts use daily.

Key Concepts You'll Learn:
- Data quality assessment
- Handling missing values
- Outlier detection and treatment
- Data validation and consistency checks
- Feature engineering for analysis
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_data(filepath='data/campaign_data_with_anomalies.csv'):
    """
    Load the campaign data from CSV file.
    
    Parameters:
    - filepath: Path to the CSV file
    
    Returns:
    - DataFrame with campaign data
    """
    
    print("📂 Loading campaign data...")
    
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Successfully loaded {len(df):,} records")
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        print("💡 Please run data_generation.py first to create the data files")
        return None

def assess_data_quality(df):
    """
    Perform comprehensive data quality assessment.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - Dictionary with quality metrics
    """
    
    print("\n🔍 Assessing Data Quality...")
    print("=" * 50)
    
    quality_report = {}
    
    # Basic info
    quality_report['total_records'] = len(df)
    quality_report['total_columns'] = len(df.columns)
    quality_report['date_range'] = f"{df['date'].min()} to {df['date'].max()}"
    
    # Missing values
    missing_data = df.isnull().sum()
    quality_report['missing_values'] = missing_data[missing_data > 0].to_dict()
    
    # Data types
    quality_report['data_types'] = df.dtypes.to_dict()
    
    # Duplicate records
    duplicates = df.duplicated().sum()
    quality_report['duplicate_records'] = duplicates
    
    # Unique values
    quality_report['unique_campaigns'] = df['campaign_id'].nunique()
    quality_report['unique_devices'] = df['device'].nunique()
    quality_report['unique_locations'] = df['location'].nunique()
    
    # Print summary
    print(f"📊 Total Records: {quality_report['total_records']:,}")
    print(f"📅 Date Range: {quality_report['date_range']}")
    print(f"🎯 Campaigns: {quality_report['unique_campaigns']}")
    print(f"📱 Devices: {quality_report['unique_devices']}")
    print(f"📍 Locations: {quality_report['unique_locations']}")
    
    if quality_report['missing_values']:
        print(f"\n⚠️ Missing Values Found:")
        for col, count in quality_report['missing_values'].items():
            percentage = (count / len(df)) * 100
            print(f"   {col}: {count:,} ({percentage:.1f}%)")
    else:
        print("✅ No missing values found")
    
    if quality_report['duplicate_records'] > 0:
        print(f"⚠️ Duplicate Records: {quality_report['duplicate_records']:,}")
    else:
        print("✅ No duplicate records found")
    
    return quality_report

def clean_data(df):
    """
    Clean the campaign data by handling various data quality issues.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - Cleaned DataFrame
    """
    
    print("\n🧹 Cleaning Data...")
    print("=" * 50)
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # 1. Convert date column to datetime
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    
    # 2. Remove duplicate records
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_count - len(df_clean)
    if duplicates_removed > 0:
        print(f"🗑️ Removed {duplicates_removed} duplicate records")
    
    # 3. Handle missing values
    print("\n🔧 Handling Missing Values:")
    
    # For numeric columns, fill with median or 0
    numeric_columns = ['impressions', 'clicks', 'conversions', 'cost', 'revenue']
    
    for col in numeric_columns:
        if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
            missing_count = df_clean[col].isnull().sum()
            
            if col in ['impressions', 'clicks']:
                # Fill with 0 for these metrics
                df_clean[col] = df_clean[col].fillna(0)
                print(f"   {col}: Filled {missing_count} missing values with 0")
            else:
                # Fill with median for cost and revenue
                median_val = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_val)
                print(f"   {col}: Filled {missing_count} missing values with median ({median_val:.2f})")
    
    # 4. Handle outliers and data errors
    print("\n🔍 Handling Outliers and Data Errors:")
    
    # Remove negative values (impossible in advertising)
    for col in ['impressions', 'clicks', 'conversions', 'cost', 'revenue']:
        if col in df_clean.columns:
            negative_count = (df_clean[col] < 0).sum()
            if negative_count > 0:
                df_clean = df_clean[df_clean[col] >= 0]
                print(f"   {col}: Removed {negative_count} negative values")
    
    # Handle extreme outliers using IQR method
    for col in ['impressions', 'clicks', 'cost']:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
            if outliers > 0:
                # Cap outliers instead of removing them
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
                print(f"   {col}: Capped {outliers} outliers using IQR method")
    
    # 5. Recalculate derived metrics
    print("\n📊 Recalculating Derived Metrics:")
    
    # Ensure we don't divide by zero and handle NaN values
    df_clean['ctr'] = np.where(
        df_clean['impressions'] > 0,
        (df_clean['clicks'] / df_clean['impressions'] * 100).round(2),
        0
    )
    df_clean['ctr'] = df_clean['ctr'].fillna(0)
    
    df_clean['cpc'] = np.where(
        df_clean['clicks'] > 0,
        (df_clean['cost'] / df_clean['clicks']).round(2),
        0
    )
    df_clean['cpc'] = df_clean['cpc'].fillna(0)
    
    df_clean['cpa'] = np.where(
        df_clean['conversions'] > 0,
        (df_clean['cost'] / df_clean['conversions']).round(2),
        0
    )
    df_clean['cpa'] = df_clean['cpa'].fillna(0)
    
    df_clean['roas'] = np.where(
        df_clean['cost'] > 0,
        (df_clean['revenue'] / df_clean['cost']).round(2),
        0
    )
    df_clean['roas'] = df_clean['roas'].fillna(0)
    
    df_clean['conversion_rate'] = np.where(
        df_clean['clicks'] > 0,
        (df_clean['conversions'] / df_clean['clicks'] * 100).round(2),
        0
    )
    df_clean['conversion_rate'] = df_clean['conversion_rate'].fillna(0)
    
    print("   ✅ All KPIs recalculated")
    
    # 6. Data validation
    print("\n✅ Data Validation:")
    
    # Check for logical inconsistencies
    invalid_ctr = (df_clean['ctr'] > 100).sum()
    if invalid_ctr > 0:
        print(f"   ⚠️ Found {invalid_ctr} records with CTR > 100%")
        df_clean['ctr'] = df_clean['ctr'].clip(upper=100)
    
    invalid_cvr = (df_clean['conversion_rate'] > 100).sum()
    if invalid_cvr > 0:
        print(f"   ⚠️ Found {invalid_cvr} records with Conversion Rate > 100%")
        df_clean['conversion_rate'] = df_clean['conversion_rate'].clip(upper=100)
    
    print("   ✅ All logical checks passed")
    
    return df_clean

def add_features(df):
    """
    Add useful features for analysis.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - DataFrame with additional features
    """
    
    print("\n🔧 Adding Analysis Features...")
    
    df_features = df.copy()
    
    # 1. Time-based features
    df_features['day_of_week'] = df_features['date'].dt.day_name()
    df_features['month'] = df_features['date'].dt.month
    df_features['week'] = df_features['date'].dt.isocalendar().week
    df_features['is_weekend'] = df_features['date'].dt.weekday >= 5
    
    # 2. Performance categories
    df_features['ctr_category'] = pd.cut(
        df_features['ctr'], 
        bins=[0, 1, 2, 5, 100], 
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    df_features['roas_category'] = pd.cut(
        df_features['roas'], 
        bins=[0, 1, 2, 5, 100], 
        labels=['Poor', 'Break-even', 'Good', 'Excellent']
    )
    
    # 3. Cost efficiency
    df_features['cost_per_impression'] = (df_features['cost'] / df_features['impressions']).round(4)
    
    # 4. Revenue efficiency
    df_features['revenue_per_click'] = np.where(
        df_features['clicks'] > 0,
        (df_features['revenue'] / df_features['clicks']).round(2),
        0
    )
    
    print("   ✅ Added time-based features")
    print("   ✅ Added performance categories")
    print("   ✅ Added efficiency metrics")
    
    return df_features

def validate_cleaned_data(df):
    """
    Validate the cleaned data to ensure quality.
    
    Parameters:
    - df: Input DataFrame
    
    Returns:
    - Boolean indicating if data is valid
    """
    
    print("\n✅ Final Data Validation...")
    
    issues = []
    
    # Check for missing values in base metrics only
    base_metrics = ['impressions', 'clicks', 'conversions', 'cost', 'revenue']
    missing_base = df[base_metrics].isnull().sum().sum()
    if missing_base > 0:
        issues.append(f"Still have {missing_base} missing values in base metrics")
    
    # Check for negative values
    numeric_cols = ['impressions', 'clicks', 'conversions', 'cost', 'revenue']
    for col in numeric_cols:
        if col in df.columns and (df[col] < 0).any():
            issues.append(f"Found negative values in {col}")
    
    # Check for impossible KPIs
    if (df['ctr'] > 100).any():
        issues.append("Found CTR values > 100%")
    
    if (df['conversion_rate'] > 100).any():
        issues.append("Found Conversion Rate values > 100%")
    
    # Check date range
    if df['date'].min() > df['date'].max():
        issues.append("Date range is invalid")
    
    if issues:
        print("   ⚠️ Issues found:")
        for issue in issues:
            print(f"      - {issue}")
        return False
    else:
        print("   ✅ All validation checks passed")
        return True

def save_processed_data(df, filename='campaign_data_processed.csv'):
    """
    Save the processed data to a CSV file.
    
    Parameters:
    - df: DataFrame to save
    - filename: Output filename
    """
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    filepath = os.path.join('data', filename)
    df.to_csv(filepath, index=False)
    
    print(f"\n💾 Processed data saved to {filepath}")
    print(f"📁 File size: {os.path.getsize(filepath) / 1024:.1f} KB")
    
    return filepath

def generate_processing_summary(df_original, df_cleaned):
    """
    Generate a summary of the data processing steps.
    
    Parameters:
    - df_original: Original DataFrame
    - df_cleaned: Cleaned DataFrame
    """
    
    print("\n📈 Processing Summary:")
    print("=" * 50)
    
    print(f"Original Records: {len(df_original):,}")
    print(f"Cleaned Records: {len(df_cleaned):,}")
    print(f"Records Removed: {len(df_original) - len(df_cleaned):,}")
    
    print(f"\nData Quality Improvements:")
    print(f"  - Missing values: {df_original.isnull().sum().sum()} → {df_cleaned.isnull().sum().sum()}")
    print(f"  - Duplicates: {df_original.duplicated().sum()} → {df_cleaned.duplicated().sum()}")
    
    print(f"\nKPI Ranges (Cleaned Data):")
    print(f"  - CTR: {df_cleaned['ctr'].min():.2f}% - {df_cleaned['ctr'].max():.2f}%")
    print(f"  - CPC: ${df_cleaned['cpc'].min():.2f} - ${df_cleaned['cpc'].max():.2f}")
    print(f"  - ROAS: {df_cleaned['roas'].min():.2f}x - {df_cleaned['roas'].max():.2f}x")

if __name__ == "__main__":
    """
    Main execution block - this runs when you execute the script directly.
    """
    
    print("🚀 Starting Ad Campaign Data Processing")
    print("=" * 50)
    
    # Load data
    df = load_data()
    if df is None:
        exit(1)
    
    # Assess data quality
    quality_report = assess_data_quality(df)
    
    # Clean data
    df_cleaned = clean_data(df)
    
    # Add features
    df_processed = add_features(df_cleaned)
    
    # Validate cleaned data
    is_valid = validate_cleaned_data(df_processed)
    
    if is_valid:
        # Save processed data
        processed_file = save_processed_data(df_processed)
        
        # Generate summary
        generate_processing_summary(df, df_processed)
        
        print("\n🎉 Data processing complete!")
        print("📁 Files created:")
        print(f"   - {processed_file} (processed data)")
        
        print("\n💡 Next steps:")
        print("   1. Run analysis.py to calculate insights")
        print("   2. Run dashboard.py to view the interactive dashboard")
    else:
        print("\n❌ Data validation failed. Please check the issues above.") 