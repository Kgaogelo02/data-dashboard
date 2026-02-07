"""
Data Dashboard Application - Main Streamlit App
Interactive web-based dashboard for data exploration and visualization.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Fixed for visibility
st.markdown("""
    <style>
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    /* Force metric text to be visible */
    div[data-testid="stMetricValue"] {
        color: #0e1117 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #1f77b4 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #31333F !important;
        font-size: 1rem !important;
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #31373F !important;
    }
    
    /* Make sure all metric text is dark */
    [data-testid="stMetric"] * {
        color: #0e1187 !important;
    }
    
    /* Ensure sidebar is visible */
    [data-testid="stSidebar"] {
        background-color: #add8e6;
    }
    
    /* Better spacing */
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_database_manager():
    """Get cached database manager instance."""
    from src.database import DatabaseManager
    return DatabaseManager('data/dashboard.db')

@st.cache_resource
def get_analyzer():
    """Get cached data analyzer instance."""
    from src.analytics import DataAnalyzer
    db_manager = get_database_manager()
    return DataAnalyzer(db_manager)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">📊 Data Dashboard Application</div>', 
                unsafe_allow_html=True)
    st.markdown("Explore, analyze, and visualize your data with interactive charts and filters.")
    st.markdown("---")
    
    # ==================== DATABASE AUTO-INITIALIZATION ====================
    # Check if database exists, if not create it automatically
    if not os.path.exists('data/dashboard.db'):
        st.info("🔄 **Initializing database for the first time...**")
        
        # Create necessary directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('exports', exist_ok=True)
        
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Create database
            status_text.text("Step 1/6: Creating database tables...")
            from src.database import DatabaseManager
            db_manager = DatabaseManager('data/dashboard.db')
            progress_bar.progress(20)
            
            # Step 2: Generate sales data
            status_text.text("Step 2/6: Generating sample sales data...")
            from src.data_utils import DataGenerator
            sales_df = DataGenerator.generate_sales_data(1000)  # Smaller dataset for faster loading
            progress_bar.progress(40)
            
            # Step 3: Clean data
            status_text.text("Step 3/6: Cleaning and validating data...")
            from src.data_utils import DataCleaner
            sales_df = DataCleaner.clean_sales_data(sales_df)
            progress_bar.progress(60)
            
            # Step 4: Generate reference data
            status_text.text("Step 4/6: Creating reference tables...")
            region_df = DataGenerator.generate_region_data()
            category_df = DataGenerator.generate_category_data()
            progress_bar.progress(80)
            
            # Step 5: Load all data
            status_text.text("Step 5/6: Loading data into database...")
            from src.data_utils import DataLoader
            loader = DataLoader(db_manager)
            loader.load_sales_data(sales_df)
            loader.load_region_data(region_df)
            loader.load_category_data(category_df)
            progress_bar.progress(100)
            
            # Step 6: Success message
            status_text.text("✅ Database initialized successfully!")
            st.success("**Database ready! Refreshing dashboard...**")
            
            # Wait 2 seconds and refresh
            import time
            time.sleep(2)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ **Error initializing database:** {str(e)}")
            st.info("""
            **Troubleshooting:**
            1. Check if all dependencies are installed
            2. Verify file permissions
            3. Try refreshing the page
            """)
            st.stop()
    
    # Initialize analyzer
    try:
        analyzer = get_analyzer()
        from src.visualizations import Visualizer
        visualizer = Visualizer()
    except Exception as e:
        st.error(f"❌ **Error connecting to database:** {e}")
        st.info("The database exists but cannot be accessed.")
        
        # Add a retry button
        if st.button("🔄 Retry Database Connection"):
            st.rerun()
        
        # Add option to recreate database
        if st.button("🗑️ Recreate Database (Delete and Start Over)"):
            if os.path.exists('data/dashboard.db'):
                os.remove('data/dashboard.db')
            st.rerun()
        
        st.stop()
    
    # ==================== SIDEBAR - FILTERS ====================
    with st.sidebar:
        st.header("🔍 Filters")
        st.markdown("---")
        
        # Date range filter
        st.subheader("📅 Date Range")
        date_option = st.radio(
            "Select period:",
            ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time", "Custom"],
            index=1  # Default to Last 90 Days
        )
        
        today = datetime.now()
        if date_option == "Last 30 Days":
            start_date = today - timedelta(days=30)
            end_date = today
        elif date_option == "Last 90 Days":
            start_date = today - timedelta(days=90)
            end_date = today
        elif date_option == "Last 6 Months":
            start_date = today - timedelta(days=180)
            end_date = today
        elif date_option == "Last Year":
            start_date = today - timedelta(days=365)
            end_date = today
        elif date_option == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start", today - timedelta(days=90))
            with col2:
                end_date = st.date_input("End", today)
            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = datetime.combine(end_date, datetime.max.time())
        else:  # All Time
            start_date = None
            end_date = None
        
        st.markdown("---")
        
        # Category filter
        st.subheader("📦 Categories")
        all_categories = ['Electronics', 'Clothing', 'Food & Beverage', 'Home & Garden', 'Sports & Outdoors']
        selected_categories = st.multiselect(
            "Select categories:",
            all_categories,
            default=all_categories
        )
        
        st.markdown("---")
        
        # Region filter
        st.subheader("🌍 Regions")
        all_regions = ['North America', 'Europe', 'Asia Pacific', 'Africa', 'Latin America', 'Middle East', 'Oceania']
        selected_regions = st.multiselect(
            "Select regions:",
            all_regions,
            default=all_regions
        )
        
        st.markdown("---")
        
        # Customer segment filter
        st.subheader("👥 Customer Segments")
        all_segments = ['Consumer', 'Corporate', 'Home Office']
        selected_segments = st.multiselect(
            "Select segments:",
            all_segments,
            default=all_segments
        )
    
    # Apply filters (convert empty lists to None)
    filter_categories = selected_categories if selected_categories else None
    filter_regions = selected_regions if selected_regions else None
    filter_segments = selected_segments if selected_segments else None
    
    # Get summary statistics
    summary = analyzer.get_sales_summary(
        start_date, end_date, 
        filter_categories, filter_regions, filter_segments
    )
    
    # ==================== KEY METRICS ====================
    st.header("📈 Key Metrics")
    
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Total Revenue",
                value=f"${summary['total_revenue']:,.2f}"
            )
        
        with col2:
            st.metric(
                label="🛒 Total Transactions",
                value=f"{summary['total_transactions']:,}"
            )
        
        with col3:
            st.metric(
                label="📊 Avg Transaction Value",
                value=f"${summary['avg_transaction_value']:,.2f}"
            )
        
        with col4:
            st.metric(
                label="📦 Units Sold",
                value=f"{summary['total_quantity_sold']:,}"
            )
    else:
        st.warning("⚠️ No data available for the selected filters. Try adjusting your filter selections.")
    
    st.markdown("---")
    
    # ==================== REVENUE TRENDS ====================
    st.header("📊 Revenue Trends")
    
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        # Daily trend
        daily_trend = analyzer.get_daily_revenue_trend(start_date, end_date)
        if not daily_trend.empty:
            # Limit to last 90 days for better visualization
            if len(daily_trend) > 90:
                daily_trend = daily_trend.tail(90)
            fig_daily = visualizer.create_revenue_line_chart(
                daily_trend, 'date', 'revenue', 
                "Daily Revenue Trend (Last 90 Days)"
            )
            st.plotly_chart(fig_daily, use_container_width=True)
        else:
            st.info("📭 No daily trend data available for selected filters")
    
    with trend_col2:
        # Monthly trend
        monthly_trend = analyzer.get_monthly_revenue_trend(start_date, end_date)
        if not monthly_trend.empty:
            fig_monthly = visualizer.create_revenue_line_chart(
                monthly_trend, 'month', 'revenue',
                "Monthly Revenue Trend"
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.info("📭 No monthly trend data available for selected filters")
    
    st.markdown("---")
    
    # ==================== CATEGORY & REGION ANALYSIS ====================
    st.header("🎯 Category & Region Analysis")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.subheader("By Category")
        # Revenue by category
        category_revenue = analyzer.get_revenue_by_category(start_date, end_date)
        if not category_revenue.empty:
            fig_category = visualizer.create_bar_chart(
                category_revenue, 'category', 'total_amount',
                "Revenue by Category"
            )
            st.plotly_chart(fig_category, use_container_width=True)
            
            # Pie chart
            fig_pie_category = visualizer.create_pie_chart(
                category_revenue, 'category', 'total_amount',
                "Category Distribution"
            )
            st.plotly_chart(fig_pie_category, use_container_width=True)
        else:
            st.info("📭 No category data available")
    
    with analysis_col2:
        st.subheader("By Region")
        # Revenue by region
        region_revenue = analyzer.get_revenue_by_region(start_date, end_date)
        if not region_revenue.empty:
            fig_region = visualizer.create_bar_chart(
                region_revenue, 'region', 'total_amount',
                "Revenue by Region", orientation='h'
            )
            st.plotly_chart(fig_region, use_container_width=True)
            
            # Pie chart
            fig_pie_region = visualizer.create_pie_chart(
                region_revenue, 'region', 'total_amount',
                "Region Distribution"
            )
            st.plotly_chart(fig_pie_region, use_container_width=True)
        else:
            st.info("📭 No region data available")
    
    st.markdown("---")
    
    # ==================== CUSTOMER SEGMENT ANALYSIS ====================
    st.header("👥 Customer Segment Analysis")
    
    segment_col1, segment_col2 = st.columns(2)
    
    with segment_col1:
        # Revenue by segment
        segment_revenue = analyzer.get_revenue_by_segment(start_date, end_date)
        if not segment_revenue.empty:
            fig_segment = visualizer.create_pie_chart(
                segment_revenue, 'customer_segment', 'total_amount',
                "Revenue by Customer Segment"
            )
            st.plotly_chart(fig_segment, use_container_width=True)
        else:
            st.info("📭 No segment data available")
    
    with segment_col2:
        # Top products
        top_products = analyzer.get_top_products(10, start_date, end_date)
        if not top_products.empty:
            fig_products = visualizer.create_bar_chart(
                top_products, 'product_name', 'total_amount',
                "Top 10 Products by Revenue", orientation='h'
            )
            st.plotly_chart(fig_products, use_container_width=True)
        else:
            st.info("📭 No product data available")
    
    st.markdown("---")
    
    # ==================== DETAILED PERFORMANCE TABLE ====================
    st.header("📋 Category Performance Details")
    
    performance = analyzer.get_category_performance(start_date, end_date)
    if not performance.empty:
        # Format the dataframe for display
        display_df = performance.copy()
        display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.2f}")
        display_df['avg_price'] = display_df['avg_price'].apply(lambda x: f"${x:,.2f}")
        display_df['avg_transaction_value'] = display_df['avg_transaction_value'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No performance data available")
    
    st.markdown("---")
    
    # ==================== EXPORT SECTION ====================
    st.header("💾 Export Data")
    st.markdown("Click any button below to download data directly to your computer")
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        sales_data = analyzer.get_sales_data(
            start_date, end_date,
            filter_categories, filter_regions, filter_segments
        )
        if not sales_data.empty:
            # Convert to CSV for download
            csv = sales_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f'sales_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )
        else:
            st.warning("⚠️ No data to export")
    
    with export_col2:
        sales_data = analyzer.get_sales_data(
            start_date, end_date,
            filter_categories, filter_regions, filter_segments
        )
        if not sales_data.empty:
            # Convert to Excel for download
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                sales_data.to_excel(writer, sheet_name='Sales Data', index=False)
            buffer.seek(0)
            
            st.download_button(
                label="📊 Download Excel",
                data=buffer,
                file_name=f'sales_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        else:
            st.warning("⚠️ No data to export")
    
    with export_col3:
        # Summary report with multiple sheets
        summary_dict = {
            'Summary': pd.DataFrame([analyzer.get_sales_summary(start_date, end_date)]).T.reset_index(),
            'By_Category': analyzer.get_revenue_by_category(start_date, end_date),
            'By_Region': analyzer.get_revenue_by_region(start_date, end_date),
            'By_Segment': analyzer.get_revenue_by_segment(start_date, end_date),
            'Top_Products': analyzer.get_top_products(20, start_date, end_date),
            'Performance': analyzer.get_category_performance(start_date, end_date)
        }
        
        # Rename summary columns
        if not summary_dict['Summary'].empty:
            summary_dict['Summary'].columns = ['Metric', 'Value']
        
        # Create Excel with multiple sheets
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for sheet_name, df in summary_dict.items():
                if not df.empty:
                    df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
        buffer.seek(0)
        
        st.download_button(
            label="📈 Download Full Report",
            data=buffer,
            file_name=f'summary_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p><strong>Data Dashboard Application</strong> | Built with Streamlit, Python, and SQLite</p>
            <p>Interactive analytics and visualization platform</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
