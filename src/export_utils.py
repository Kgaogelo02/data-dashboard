"""
Data export utilities for the dashboard.
"""

import pandas as pd
from datetime import datetime
import os

class DataExporter:
    """Export data in various formats."""
    
    @staticmethod
    def export_to_csv(df, filename=None):
        """Export DataFrame to CSV."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.csv"
        
        # Ensure exports directory exists
        os.makedirs('exports', exist_ok=True)
        filepath = os.path.join('exports', filename)
        
        df.to_csv(filepath, index=False)
        return filepath
    
    @staticmethod
    def export_to_excel(df, filename=None, sheet_name='Data'):
        """Export DataFrame to Excel."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.xlsx"
        
        # Ensure exports directory exists
        os.makedirs('exports', exist_ok=True)
        filepath = os.path.join('exports', filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets[sheet_name]
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        return filepath
    
    @staticmethod
    def export_multiple_sheets(dataframes_dict, filename=None):
        """Export multiple DataFrames to Excel with separate sheets."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_multi_{timestamp}.xlsx"
        
        # Ensure exports directory exists
        os.makedirs('exports', exist_ok=True)
        filepath = os.path.join('exports', filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in dataframes_dict.items():
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet name limit
                
                # Auto-adjust column widths
                worksheet = writer.sheets[sheet_name[:31]]
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    ) + 2
                    if idx < 26:  # Handle up to 26 columns (A-Z)
                        worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        return filepath
    
    @staticmethod
    def create_summary_report(analyzer, start_date=None, end_date=None):
        """Create a comprehensive summary report."""
        report_data = {
            'Summary': pd.DataFrame([analyzer.get_sales_summary(start_date, end_date)]).T.reset_index(),
            'Revenue_by_Category': analyzer.get_revenue_by_category(start_date, end_date),
            'Revenue_by_Region': analyzer.get_revenue_by_region(start_date, end_date),
            'Revenue_by_Segment': analyzer.get_revenue_by_segment(start_date, end_date),
            'Top_Products': analyzer.get_top_products(20, start_date, end_date),
            'Category_Performance': analyzer.get_category_performance(start_date, end_date)
        }
        
        # Rename summary columns
        if not report_data['Summary'].empty:
            report_data['Summary'].columns = ['Metric', 'Value']
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{timestamp}.xlsx"
        
        return DataExporter.export_multiple_sheets(report_data, filename)