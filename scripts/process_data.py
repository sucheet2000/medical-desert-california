#!/usr/bin/env python3
"""
Process and merge CDC PLACES and USDA Food Access data for California
Creates analysis-ready dataset for Tableau visualization
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_cdc_places():
    """Load and filter CDC PLACES data for California"""
    print("\n📂 Loading CDC PLACES data...")
    
    file_path = RAW_DATA_DIR / "cdc_places_2024_tracts.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"CDC PLACES data not found. Run download_data.py first.")
    
    # Load data
    df = pd.read_csv(file_path, low_memory=False)
    print(f"   Total records: {len(df):,}")
    
    # Filter for California only
    df_ca = df[df['StateAbbr'] == 'CA'].copy()
    print(f"   California records: {len(df_ca):,}")
    
    # Focus on key health measures
    measures_to_keep = [
        'DIABETES',      # Diabetes prevalence
        'CHD',           # Coronary heart disease
        'STROKE',        # Stroke prevalence
        'OBESITY',       # Obesity prevalence
        'BPHIGH',        # High blood pressure
        'CSMOKING',      # Current smoking
        'CHECKUP',       # Annual checkup
        'ACCESS2'        # Lack of health insurance
    ]
    
    # Filter for these measures with crude prevalence
    df_ca = df_ca[
        (df_ca['MeasureId'].isin(measures_to_keep)) &
        (df_ca['Data_Value_Type'] == 'Crude prevalence')
    ].copy()
    
    print(f"   Filtered to key health measures: {len(df_ca):,}")
    
    return df_ca

def pivot_health_data(df_ca):
    """Pivot health data to have one row per census tract"""
    print("\n🔄 Pivoting health data by census tract...")
    
    # Create pivot table - LocationID is the 11-digit Census Tract FIPS code
    pivot_df = df_ca.pivot_table(
        index=['LocationID', 'LocationName', 'CountyName'],
        columns='MeasureId',
        values='Data_Value',
        aggfunc='first'
    ).reset_index()
    
    # Rename columns for clarity
    column_mapping = {
        'DIABETES': 'diabetes_prevalence',
        'CHD': 'heart_disease_prevalence',
        'STROKE': 'stroke_prevalence',
        'OBESITY': 'obesity_prevalence',
        'BPHIGH': 'high_bp_prevalence',
        'CSMOKING': 'smoking_prevalence',
        'CHECKUP': 'annual_checkup_pct',
        'ACCESS2': 'no_insurance_pct',
        'LocationID': 'tract_fips',  # LocationID is the Census Tract FIPS
        'LocationName': 'location_name',
        'CountyName': 'county_name'
    }
    
    pivot_df = pivot_df.rename(columns=column_mapping)
    
    print(f"   Census tracts in California: {len(pivot_df):,}")
    
    return pivot_df

def load_usda_food_access():
    """Load USDA Food Access Research Atlas data"""
    print("\n📂 Loading USDA Food Access data...")
    
    file_path = RAW_DATA_DIR / "usda_food_access_2019.xlsx"
    
    if not file_path.exists():
        raise FileNotFoundError(f"USDA Food Access data not found. Run download_data.py first.")
    
    # Load the data
    df = pd.read_excel(file_path, sheet_name='Food Access Research Atlas')
    print(f"   Total records: {len(df):,}")
    
    # Filter for California (State code 06)
    df_ca = df[df['State'] == 'California'].copy()
    print(f"   California records: {len(df_ca):,}")
    
    # Keep relevant columns
    columns_to_keep = [
        'CensusTract',           # FIPS code (11 digits)
        'State',
        'County',
        'Urban',                  # 1 = urban, 0 = rural
        'LILATracts_1And10',     # Low Income Low Access (1 mile urban / 10 miles rural)
        'LILATracts_halfAnd10',  # More strict definition
        'LILATracts_1And20',     # Very rural definition
        'lapophalf',             # Population beyond 1/2 mile (urban)
        'lapop1',                # Population beyond 1 mile
        'lapop10',               # Population beyond 10 miles
        'lalowihalf',            # Low income pop beyond 1/2 mile
        'lalowi1',               # Low income pop beyond 1 mile
        'lalowi10'               # Low income pop beyond 10 miles
    ]
    
    df_ca = df_ca[columns_to_keep].copy()
    
    # Ensure FIPS code is properly formatted (11 digits with leading zeros)
    df_ca['tract_fips'] = df_ca['CensusTract'].astype(str).str.zfill(11)
    
    return df_ca

def merge_datasets(health_df, food_df):
    """Merge health and food access data on FIPS codes"""
    print("\n🔗 Merging health and food access data...")
    
    # Ensure FIPS codes are formatted consistently
    health_df['tract_fips'] = health_df['tract_fips'].astype(str).str.zfill(11)
    food_df['tract_fips'] = food_df['tract_fips'].astype(str).str.zfill(11)
    
    # Merge on FIPS code
    merged_df = health_df.merge(
        food_df,
        on='tract_fips',
        how='left'  # Keep all health data, even if no food access data
    )
    
    print(f"   Merged records: {len(merged_df):,}")
    print(f"   Tracts with food access data: {merged_df['LILATracts_1And10'].notna().sum():,}")
    
    return merged_df

def calculate_risk_scores(df):
    """Calculate composite healthcare desert risk scores"""
    print("\n📊 Calculating Healthcare Desert Risk Scores...")
    
    # Fill NaN values for food access (assume not a food desert if no data)
    df['LILATracts_1And10'] = df['LILATracts_1And10'].fillna(0)
    df['Urban'] = df['Urban'].fillna(1)  # Assume urban if missing
    
    # Calculate composite health risk score (0-100 scale)
    # Higher score = worse health outcomes
    health_measures = [
        'diabetes_prevalence',
        'heart_disease_prevalence',
        'obesity_prevalence',
        'high_bp_prevalence',
        'no_insurance_pct'
    ]
    
    # Simple average of available measures
    df['health_risk_score'] = df[health_measures].mean(axis=1)
    
    # Create risk categories
    df['health_risk_category'] = pd.cut(
        df['health_risk_score'],
        bins=[0, 10, 15, 20, 100],
        labels=['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
    )
    
    # Create combined risk flag
    df['is_food_desert'] = df['LILATracts_1And10'] == 1
    df['combined_risk'] = 'Low Risk'
    
    df.loc[
        (df['health_risk_score'] > 15) & (df['is_food_desert']),
        'combined_risk'
    ] = 'High Risk: Desert + Disease'
    
    df.loc[
        (df['health_risk_score'] > 15) & (~df['is_food_desert']),
        'combined_risk'
    ] = 'High Risk: Disease Only'
    
    df.loc[
        (df['health_risk_score'] <= 15) & (df['is_food_desert']),
        'combined_risk'
    ] = 'Moderate Risk: Desert Only'
    
    print(f"\n   Risk Distribution:")
    print(df['combined_risk'].value_counts())
    
    return df

def focus_on_santa_clara(df):
    """Create a separate dataset focused on Santa Clara County"""
    print("\n🎯 Creating Santa Clara County focused dataset...")
    
    df_sc = df[df['county_name'].str.contains('Santa Clara', case=False, na=False)].copy()
    
    print(f"   Santa Clara County census tracts: {len(df_sc):,}")
    
    if len(df_sc) > 0:
        output_path = PROCESSED_DATA_DIR / "santa_clara_health_equity.csv"
        df_sc.to_csv(output_path, index=False)
        print(f"   ✅ Saved to: {output_path}")
    
    return df_sc

def main():
    """Main data processing pipeline"""
    print("="*60)
    print("🏥 MEDICAL DESERT DATA PROCESSING")
    print("="*60)
    
    try:
        # Step 1: Load CDC PLACES data
        health_df = load_cdc_places()
        
        # Step 2: Pivot health data
        health_pivot = pivot_health_data(health_df)
        
        # Step 3: Load USDA Food Access data
        food_df = load_usda_food_access()
        
        # Step 4: Merge datasets
        merged_df = merge_datasets(health_pivot, food_df)
        
        # Step 5: Calculate risk scores
        final_df = calculate_risk_scores(merged_df)
        
        # Step 6: Save full California dataset
        output_path = PROCESSED_DATA_DIR / "california_health_equity.csv"
        final_df.to_csv(output_path, index=False)
        print(f"\n✅ Full California dataset saved to: {output_path}")
        
        # Step 7: Create Santa Clara focused dataset
        sc_df = focus_on_santa_clara(final_df)
        
        # Summary statistics
        print("\n" + "="*60)
        print("📊 DATA SUMMARY")
        print("="*60)
        print(f"Total California census tracts: {len(final_df):,}")
        print(f"Santa Clara County tracts: {len(sc_df):,}")
        print(f"Food deserts identified: {final_df['is_food_desert'].sum():,}")
        print(f"High-risk tracts: {(final_df['combined_risk'] == 'High Risk: Desert + Disease').sum():,}")
        
        print("\n🎉 Data processing complete!")
        print("\nNext steps:")
        print("1. Open Tableau Public")
        print("2. Load: data/processed/california_health_equity.csv")
        print("3. Start building your visualization!")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Please run download_data.py first to download the required datasets.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()
