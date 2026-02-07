"""
Data query and analysis functions for the dashboard.
"""

import pandas as pd
from sqlalchemy import func, and_, or_
from src.database import SalesData, RegionInfo, ProductCategory

class DataAnalyzer:
    """Analyze data from the database."""
    
    def __init__(self, db_manager):
        """Initialize with database manager."""
        self.db_manager = db_manager
    
    def get_sales_data(self, start_date=None, end_date=None, categories=None, 
                       regions=None, segments=None):
        """Query sales data with filters."""
        session = self.db_manager.get_session()
        try:
            query = session.query(SalesData)
            
            # Apply filters
            filters = []
            if start_date:
                filters.append(SalesData.transaction_date >= start_date)
            if end_date:
                filters.append(SalesData.transaction_date <= end_date)
            if categories:
                filters.append(SalesData.category.in_(categories))
            if regions:
                filters.append(SalesData.region.in_(regions))
            if segments:
                filters.append(SalesData.customer_segment.in_(segments))
            
            if filters:
                query = query.filter(and_(*filters))
            
            # Convert to DataFrame
            df = pd.read_sql(query.statement, session.bind)
            return df
        finally:
            session.close()
    
    def get_sales_summary(self, start_date=None, end_date=None, categories=None,
                         regions=None, segments=None):
        """Get summary statistics for sales data."""
        df = self.get_sales_data(start_date, end_date, categories, regions, segments)
        
        if df.empty:
            return {}
        
        summary = {
            'total_revenue': df['total_amount'].sum(),
            'total_transactions': len(df),
            'avg_transaction_value': df['total_amount'].mean(),
            'total_quantity_sold': df['quantity'].sum(),
            'unique_products': df['product_name'].nunique(),
            'unique_categories': df['category'].nunique()
        }
        return summary
    
    def get_revenue_by_category(self, start_date=None, end_date=None):
        """Get revenue grouped by category."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('category')['total_amount'].sum().reset_index()\
                 .sort_values('total_amount', ascending=False)
    
    def get_revenue_by_region(self, start_date=None, end_date=None):
        """Get revenue grouped by region."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('region')['total_amount'].sum().reset_index()\
                 .sort_values('total_amount', ascending=False)
    
    def get_revenue_by_segment(self, start_date=None, end_date=None):
        """Get revenue grouped by customer segment."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('customer_segment')['total_amount'].sum().reset_index()\
                 .sort_values('total_amount', ascending=False)
    
    def get_daily_revenue_trend(self, start_date=None, end_date=None):
        """Get daily revenue trend."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        df['date'] = pd.to_datetime(df['transaction_date']).dt.date
        daily = df.groupby('date')['total_amount'].sum().reset_index()
        daily.columns = ['date', 'revenue']
        return daily.sort_values('date')
    
    def get_monthly_revenue_trend(self, start_date=None, end_date=None):
        """Get monthly revenue trend."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        df['month'] = pd.to_datetime(df['transaction_date']).dt.to_period('M')
        monthly = df.groupby('month')['total_amount'].sum().reset_index()
        monthly['month'] = monthly['month'].astype(str)
        monthly.columns = ['month', 'revenue']
        return monthly.sort_values('month')
    
    def get_top_products(self, n=10, start_date=None, end_date=None):
        """Get top N products by revenue."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('product_name')['total_amount'].sum().reset_index()\
                 .sort_values('total_amount', ascending=False).head(n)
    
    def get_category_performance(self, start_date=None, end_date=None):
        """Get detailed performance metrics by category."""
        df = self.get_sales_data(start_date, end_date)
        if df.empty:
            return pd.DataFrame()
        
        performance = df.groupby('category').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'id': 'count',
            'unit_price': 'mean'
        }).reset_index()
        
        performance.columns = ['category', 'revenue', 'units_sold', 
                              'transactions', 'avg_price']
        performance['avg_transaction_value'] = performance['revenue'] / performance['transactions']
        
        return performance.sort_values('revenue', ascending=False)
    
    def get_region_info(self):
        """Get region information."""
        session = self.db_manager.get_session()
        try:
            df = pd.read_sql(session.query(RegionInfo).statement, session.bind)
            return df
        finally:
            session.close()
    
    def get_category_info(self):
        """Get category information."""
        session = self.db_manager.get_session()
        try:
            df = pd.read_sql(session.query(ProductCategory).statement, session.bind)
            return df
        finally:
            session.close()