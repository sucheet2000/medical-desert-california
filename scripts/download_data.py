#!/usr/bin/env python3
"""
Download CDC PLACES, USDA Food Access, and NPPES Provider data for California
Author: Medical Desert Analysis Project
"""

import requests
import pandas as pd
import os
from pathlib import Path
import zipfile
import io

# Project paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, destination, description):
    """Download a file with progress indication"""
    print(f"\n📥 Downloading {description}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✅ Downloaded to: {destination}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading {description}: {e}")
        return False

def download_cdc_places():
    """Download CDC PLACES 2024 Census Tract Data"""
    # CDC PLACES 2024 Release - Census Tract Level
    # This is the most granular health data available
    url = "https://data.cdc.gov/api/views/cwsq-ngmh/rows.csv?accessType=DOWNLOAD"
    destination = RAW_DATA_DIR / "cdc_places_2024_tracts.csv"
    
    success = download_file(url, destination, "CDC PLACES 2024 (Census Tract)")
    
    if success:
        print(f"📊 File size: {os.path.getsize(destination) / (1024*1024):.1f} MB")
    
    return success

def download_usda_food_access():
    """Download USDA Food Access Research Atlas"""
    # USDA Food Access Research Atlas (2019)
    # Contains Low Income Low Access (LILA) tract designations
    url = "https://ers.usda.gov/sites/default/files/_laserfiche/DataFiles/80591/FoodAccessResearchAtlasData2019.xlsx?v=57750"
    destination = RAW_DATA_DIR / "usda_food_access_2019.xlsx"
    
    success = download_file(url, destination, "USDA Food Access Atlas 2019")
    
    if success:
        print(f"📊 File size: {os.path.getsize(destination) / (1024*1024):.1f} MB")
    
    return success

def download_nppes_providers():
    """Download and filter NPPES NPI Registry for California Family Medicine providers"""
    print("\n📥 Downloading NPPES NPI Registry (this may take a while - it's a large file)...")
    
    # NPPES publishes weekly data file
    # Using the dissemination file (CSV format)
    url = "https://download.cms.gov/nppes/NPPES_Data_Dissemination_Week_1_January_2025.zip"
    
    print("\n⚠️  WARNING: The full NPPES file is 9GB+")
    print("   We'll download and filter for California Family Medicine providers only.\n")
    
    destination = RAW_DATA_DIR / "nppes_full.zip"
    
    # Note: Due to the massive size, we'll provide instructions instead of full download
    print("\n💡 ALTERNATIVE APPROACH (Recommended):")
    print("   Instead of downloading the full 9GB file, use the NPPES API:")
    print("   https://npiregistry.cms.hhs.gov/api/")
    print("\n   Or use the pre-filtered dataset approach below...\n")
    
    # For now, we'll create a smaller sample dataset
    # In production, you'd want to use the API or download the full file once
    print("📌 We'll use the NPI Registry API to fetch California providers...")
    
    try:
        # Using NPPES API to get California Family Medicine providers
        # Taxonomy Code 207Q00000X = Family Medicine
        providers = []
        
        # API limits to 200 results per query, we'll get first batch as sample
        api_url = "https://npiregistry.cms.hhs.gov/api/"
        params = {
            'version': '2.1',
            'state': 'CA',
            'taxonomy_description': 'Family Medicine',
            'limit': 200
        }
        
        print(f"   Querying NPI API for California Family Medicine providers...")
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' in data and data['results']:
            for provider in data['results']:
                # Extract key information
                addresses = provider.get('addresses', [])
                location_address = next((addr for addr in addresses if addr.get('address_purpose') == 'LOCATION'), {})
                
                providers.append({
                    'npi': provider.get('number'),
                    'name': f"{provider.get('basic', {}).get('first_name', '')} {provider.get('basic', {}).get('last_name', '')}".strip(),
                    'organization': provider.get('basic', {}).get('organization_name', ''),
                    'taxonomy': provider.get('taxonomies', [{}])[0].get('code', ''),
                    'taxonomy_desc': provider.get('taxonomies', [{}])[0].get('desc', ''),
                    'address': location_address.get('address_1', ''),
                    'city': location_address.get('city', ''),
                    'state': location_address.get('state', ''),
                    'postal_code': location_address.get('postal_code', ''),
                    'latitude': location_address.get('latitude', ''),
                    'longitude': location_address.get('longitude', '')
                })
            
            # Save to CSV
            df = pd.DataFrame(providers)
            output_path = RAW_DATA_DIR / "california_providers_sample.csv"
            df.to_csv(output_path, index=False)
            
            print(f"\n   ✅ Downloaded {len(providers)} provider records (sample)")
            print(f"   ✅ Saved to: {output_path}")
            print(f"\n   📊 Provider breakdown:")
            print(f"      - Organizations: {df['organization'].notna().sum()}")
            print(f"      - Individual providers: {df['name'].notna().sum()}")
            print(f"      - With coordinates: {df['latitude'].notna().sum()}")
            
            print("\n   💡 Note: This is a sample. For full coverage, download the complete NPPES file.")
            print("      Instructions: https://download.cms.gov/nppes/NPI_Files.html")
            
            return True
        else:
            print("   ⚠️  No results returned from API")
            return False
            
    except Exception as e:
        print(f"\n   ⚠️  API request failed: {e}")
        print("   You can manually download provider data later if needed.")
        return False

def main():
    """Main execution"""
    print("="*60)
    print("🏥 MEDICAL DESERT DATA DOWNLOAD")
    print("="*60)
    print(f"\nData will be saved to: {RAW_DATA_DIR}")
    
    # Download CDC PLACES
    cdc_success = download_cdc_places()
    
    # Download USDA Food Access
    usda_success = download_usda_food_access()
    
    # Download NPPES Provider Data (optional but valuable)
    provider_success = download_nppes_providers()
    
    # Summary
    print("\n" + "="*60)
    print("📋 DOWNLOAD SUMMARY")
    print("="*60)
    print(f"CDC PLACES 2024: {'✅ Success' if cdc_success else '❌ Failed'}")
    print(f"USDA Food Access: {'✅ Success' if usda_success else '❌ Failed'}")
    print(f"Provider Locations: {'✅ Success' if provider_success else '⚠️  Skipped'}")
    
    if cdc_success and usda_success:
        print("\n🎉 All data downloaded successfully!")
        print("\nNext step: Run the data processing script")
        print("👉 python scripts/process_data.py")
    else:
        print("\n⚠️  Some downloads failed. Please check the errors above.")

if __name__ == "__main__":
    main()
