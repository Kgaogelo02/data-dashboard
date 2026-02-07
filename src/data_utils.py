"""
Data generation and loading utilities for the dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from src.database import DatabaseManager, SalesData, RegionInfo, ProductCategory

class DataGenerator:
    """Generate sample data for the dashboard."""
    
    @staticmethod
    def generate_sales_data(num_records=5000):
        """Generate synthetic sales data."""
        np.random.seed(42)
        random.seed(42)
        
        categories = ['Electronics', 'Clothing', 'Food & Beverage', 'Home & Garden', 'Sports & Outdoors']
        regions = ['North America', 'Europe', 'Asia Pacific', 'Africa', 'Latin America', 'Middle East', 'Oceania']
        segments = ['Consumer', 'Corporate', 'Home Office']
        
        products = {
            'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress'],
            'Food & Beverage': ['Coffee', 'Tea', 'Snacks', 'Bottled Water', 'Energy Drink'],
            'Home & Garden': ['Plant', 'Furniture', 'Cookware', 'Bedding', 'Decor'],
            'Sports & Outdoors': ['Yoga Mat', 'Dumbbell', 'Bicycle', 'Tent', 'Running Shoes']
        }
        
        data = []
        start_date = datetime.now() - timedelta(days=730)  # 2 years of data (2024-2026)
        
        for _ in range(num_records):
            category = random.choice(categories)
            product = random.choice(products[category])
            quantity = random.randint(1, 20)
            unit_price = round(random.uniform(10, 500), 2)
            total = round(quantity * unit_price, 2)
            
            record = {
                'transaction_date': start_date + timedelta(days=random.randint(0, 730)),
                'category': category,
                'product_name': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': total,
                'region': random.choice(regions),
                'customer_segment': random.choice(segments)
            }
            data.append(record)
        
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_region_data():
        """Generate region information data."""
        regions = [
            {'region_name': 'North America', 'country': 'USA/Canada/Mexico', 'population': 580000000, 'avg_income': 68000},
            {'region_name': 'Europe', 'country': 'EU & UK', 'population': 750000000, 'avg_income': 48000},
            {'region_name': 'Asia Pacific', 'country': 'APAC Region', 'population': 4500000000, 'avg_income': 38000},
            {'region_name': 'Africa', 'country': 'African Continent', 'population': 1450000000, 'avg_income': 22000},
            {'region_name': 'Latin America', 'country': 'LATAM', 'population': 670000000, 'avg_income': 30000},
            {'region_name': 'Middle East', 'country': 'MENA Region', 'population': 450000000, 'avg_income': 45000},
            {'region_name': 'Oceania', 'country': 'Australia/NZ/Pacific', 'population': 45000000, 'avg_income': 52000}
        ]
        return pd.DataFrame(regions)
    
    @staticmethod
    def generate_category_data():
        """Generate product category data."""
        categories = [
            {'category_name': 'Electronics', 'description': 'Electronic devices and accessories', 'margin_percentage': 25.5},
            {'category_name': 'Clothing', 'description': 'Apparel and fashion items', 'margin_percentage': 45.0},
            {'category_name': 'Food & Beverage', 'description': 'Food and drink products', 'margin_percentage': 20.0},
            {'category_name': 'Home & Garden', 'description': 'Home improvement and garden items', 'margin_percentage': 35.0},
            {'category_name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear', 'margin_percentage': 30.0}
        ]
        return pd.DataFrame(categories)

class DataLoader:
    """Load data into the database."""
    
    def __init__(self, db_manager):
        """Initialize with database manager."""
        self.db_manager = db_manager
    
    def load_sales_data(self, df):
        """Load sales data into database."""
        session = self.db_manager.get_session()
        try:
            for _, row in df.iterrows():
                sale = SalesData(
                    transaction_date=row['transaction_date'],
                    category=row['category'],
                    product_name=row['product_name'],
                    quantity=row['quantity'],
                    unit_price=row['unit_price'],
                    total_amount=row['total_amount'],
                    region=row['region'],
                    customer_segment=row['customer_segment']
                )
                session.add(sale)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error loading sales data: {e}")
            return False
        finally:
            session.close()
    
    def load_region_data(self, df):
        """Load region data into database."""
        session = self.db_manager.get_session()
        try:
            for _, row in df.iterrows():
                region = RegionInfo(
                    region_name=row['region_name'],
                    country=row['country'],
                    population=row['population'],
                    avg_income=row['avg_income']
                )
                session.add(region)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error loading region data: {e}")
            return False
        finally:
            session.close()
    
    def load_category_data(self, df):
        """Load category data into database."""
        session = self.db_manager.get_session()
        try:
            for _, row in df.iterrows():
                category = ProductCategory(
                    category_name=row['category_name'],
                    description=row['description'],
                    margin_percentage=row['margin_percentage']
                )
                session.add(category)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error loading category data: {e}")
            return False
        finally:
            session.close()

class DataCleaner:
    """Clean and validate data."""
    
    @staticmethod
    def clean_sales_data(df):
        """Clean and validate sales data."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.dropna(subset=['transaction_date', 'category', 'product_name'])
        df['customer_segment'] = df['customer_segment'].fillna('Unknown')
        
        # Validate numeric columns
        df = df[df['quantity'] > 0]
        df = df[df['unit_price'] > 0]
        df = df[df['total_amount'] > 0]
        
        # Ensure consistent capitalization
        df['category'] = df['category'].str.strip().str.title()
        df['region'] = df['region'].str.strip().str.title()
        df['customer_segment'] = df['customer_segment'].str.strip().str.title()
        
        # Recalculate total_amount to ensure consistency
        df['total_amount'] = df['quantity'] * df['unit_price']
        
        return df
    
    @staticmethod
    def validate_date_range(df, date_column, start_date=None, end_date=None):
        """Validate and filter date range."""
        if start_date:
            df = df[df[date_column] >= start_date]
        if end_date:
            df = df[df[date_column] <= end_date]
        return df