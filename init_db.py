"""
Initialize the database with sample data.
Run this script once to set up the database.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import DatabaseManager
from src.data_utils import DataGenerator, DataLoader, DataCleaner

def initialize_database():
    """Initialize database with sample data."""
    print("=" * 60)
    print("Data Dashboard - Database Initialization")
    print("=" * 60)
    
    # Create database manager
    print("\n[1/6] Creating database connection...")
    db_manager = DatabaseManager('data/dashboard.db')
    
    # Initialize tables
    print("[2/6] Creating database tables...")
    db_manager.initialize_database()
    
    # Generate sample data
    print("[3/6] Generating sample sales data (5000 records)...")
    sales_df = DataGenerator.generate_sales_data(5000)
    
    print("[4/6] Generating region and category data...")
    region_df = DataGenerator.generate_region_data()
    category_df = DataGenerator.generate_category_data()
    
    # Clean data
    print("[5/6] Cleaning and validating data...")
    sales_df = DataCleaner.clean_sales_data(sales_df)
    
    # Load data
    print("[6/6] Loading data into database...")
    loader = DataLoader(db_manager)
    
    success = True
    if loader.load_sales_data(sales_df):
        print("  ✓ Sales data loaded successfully")
    else:
        print("  ✗ Failed to load sales data")
        success = False
    
    if loader.load_region_data(region_df):
        print("  ✓ Region data loaded successfully")
    else:
        print("  ✗ Failed to load region data")
        success = False
    
    if loader.load_category_data(category_df):
        print("  ✓ Category data loaded successfully")
    else:
        print("  ✗ Failed to load category data")
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ Database initialization completed successfully!")
        print(f"Database location: data/dashboard.db")
        print(f"Total records loaded: {len(sales_df)}")
    else:
        print("✗ Database initialization completed with errors")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    initialize_database()