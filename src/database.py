"""
Database models and connection handler for the Data Dashboard Application.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class SalesData(Base):
    """Sales transaction data model."""
    __tablename__ = 'sales_data'
    
    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime, nullable=False)
    category = Column(String(50), nullable=False)
    product_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    region = Column(String(50), nullable=False)
    customer_segment = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class RegionInfo(Base):
    """Region information model."""
    __tablename__ = 'region_info'
    
    id = Column(Integer, primary_key=True)
    region_name = Column(String(50), unique=True, nullable=False)
    country = Column(String(50), nullable=False)
    population = Column(Integer)
    avg_income = Column(Float)

class ProductCategory(Base):
    """Product category model."""
    __tablename__ = 'product_categories'
    
    id = Column(Integer, primary_key=True)
    category_name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    margin_percentage = Column(Float)

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path='data/dashboard.db'):
        """Initialize database connection."""
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session."""
        return self.Session()
    
    def initialize_database(self):
        """Create all tables."""
        Base.metadata.create_all(self.engine)
        
    def drop_all_tables(self):
        """Drop all tables (use with caution)."""
        Base.metadata.drop_all(self.engine)