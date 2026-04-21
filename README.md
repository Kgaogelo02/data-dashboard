#  Data Dashboard Application

A professional, production-ready Python web application for interactive data exploration, analysis, and visualization. Built with Streamlit, SQLite, and Plotly.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

##  Purpose

The Data Dashboard Application enables users to:
-  Explore large datasets with interactive filters
-  Visualize trends through dynamic charts and graphs
-  Analyze data by categories, regions, and time periods
-  Export filtered data and generate comprehensive reports
-  Gain insights through professional visualizations

##  Key Features

### 1. **Interactive Dashboard**
- Real-time filtering by date ranges, categories, regions, and customer segments
- Dynamic charts that update instantly based on user selections
- Responsive design that works on desktop and mobile devices

### 2. **Database Integration**
- SQLite database for efficient data storage and querying
- Support for multiple related tables (sales, regions, categories)
- Optimized queries for fast performance

### 3. **Data Processing & Validation**
- Automatic data cleaning to remove duplicates
- Missing value handling with intelligent defaults
- Data consistency validation and correction

### 4. **Dynamic Visualizations**
- **Line Charts**: Daily and monthly revenue trends
- **Bar Charts**: Category and region performance
- **Pie Charts**: Distribution analysis
- **Interactive Tables**: Detailed performance metrics
- All charts built with Plotly for interactivity

### 5. **Backend Logic**
- Efficient SQL queries with SQLAlchemy ORM
- Smart data aggregation and summarization
- Filter management without page reloads

### 6. **Export & Reporting**
- Export filtered data to CSV format
- Export to Excel with formatted columns
- Generate comprehensive multi-sheet summary reports
- Timestamped file naming for easy tracking

##  Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **IDE** | VS Code | Development environment |
| **Language** | Python 3.11+ | Core programming |
| **Web Framework** | Streamlit | Interactive web interface |
| **Database** | SQLite | Data storage |
| **ORM** | SQLAlchemy | Database management |
| **Data Processing** | Pandas | Data manipulation |
| **Visualization** | Plotly | Interactive charts |
| **Export** | openpyxl | Excel file generation |

##  Project Structure

```
data-dashboard/
│
├── app.py                  # Main Streamlit application
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
│
├── src/                   # Core application modules
│   ├── __init__.py       # Package initialization
│   ├── database.py       # Database models and connection
│   ├── data_utils.py     # Data generation and cleaning
│   ├── analytics.py      # Data analysis functions
│   ├── visualizations.py # Chart creation utilities
│   └── export_utils.py   # Data export functions
│
├── data/                  # Database storage
│   └── dashboard.db      # SQLite database (created on init)
│
├── exports/               # Exported files directory
│   └── (generated files)
│
├── assets/                # Static assets (if any)
│
|── tests/                 # Unit tests
```

##  Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd data-dashboard
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```bash
   python init_db.py
   ```
   
   This will:
   - Create the SQLite database
   - Generate 5,000 sample sales records
   - Load region and category reference data
   - Validate and clean all data

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Open Your Browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

##  Usage Guide

### Filtering Data

1. **Date Range Selection**
   - Use the sidebar to select predefined periods (Last 30 Days, Last Year, etc.)
   - Or choose "Custom" for specific date ranges

2. **Category Filtering**
   - Select one or more product categories
   - Deselect all to see all categories

3. **Region Filtering**
   - Filter by geographic regions
   - Combine with other filters for deeper insights

4. **Customer Segment Filtering**
   - Analyze different customer types
   - Compare Consumer vs Corporate performance

### Viewing Visualizations

- **Key Metrics**: Top cards show summary statistics
- **Trends**: Line charts display daily and monthly patterns
- **Comparisons**: Bar and pie charts show category/region breakdowns
- **Details**: Tables provide granular performance data

### Exporting Data

1. **CSV Export**: Raw data in comma-separated format
2. **Excel Export**: Formatted spreadsheet with auto-sized columns
3. **Summary Report**: Multi-sheet Excel with all key metrics


##  Sample Dataset

The application includes a rich synthetic dataset with:

- **5,000 transaction records** spanning 2 years
- **5 product categories**: Electronics, Clothing, Food & Beverage, Home & Garden, Sports & Outdoors
- **7 geographic regions**: North America, Europe, Asia Pacific, Africa, Latin America, Middle East, Oceania
- **3 customer segments**: Consumer, Corporate, Home Office
- **Realistic pricing** and quantity variations
- **Seasonal patterns** and trends

##  Customization

### Using Your Own Data

1. **Prepare Your Data**
   - Create a CSV or Excel file with columns matching the schema
   - Required columns: transaction_date, category, product_name, quantity, unit_price, region

2. **Modify Database Models**
   - Edit `src/database.py` to match your schema
   - Update field names and types as needed

3. **Create a Custom Loader**
   - Modify `src/data_utils.py` to load your data
   - Or use the existing DataLoader with a Pandas DataFrame

4. **Run Database Migration**
   ```bash
   python init_db.py
   ```

### Adding New Visualizations

1. Open `src/visualizations.py`
2. Add new methods to the `Visualizer` class
3. Use the new visualizations in `app.py`

Example:
```python
def create_custom_chart(df, x_col, y_col):
    fig = px.scatter(df, x=x_col, y=y_col)
    return fig
```

##  Testing

Run the test suite (when implemented):
```bash
pytest tests/
```

##  Performance Optimization

The application is optimized for:
- **Fast queries**: Indexed database columns
- **Efficient caching**: Streamlit's `@st.cache_resource` decorator
- **Lazy loading**: Data loaded only when needed
- **Responsive UI**: Minimal blocking operations

##  Troubleshooting

### Database Not Found
**Error**: "Database not found! Please run init_db.py"
**Solution**: Run `python init_db.py` to create the database

### Import Errors
**Error**: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Port Already in Use
**Error**: "Port 8501 is already in use"
**Solution**: 
- Close other Streamlit applications
- Or run with a different port: `streamlit run app.py --server.port 8502`

### Slow Performance
**Issue**: Dashboard loads slowly
**Solution**:
- Reduce the date range in filters
- Use predefined periods instead of "All Time"
- Clear Streamlit cache: Press 'C' in the app and select "Clear cache"

##  Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


##  Future Enhancements

Potential features for future versions:
- [ ] User authentication and multi-user support
- [ ] Real-time data updates
- [ ] Advanced statistical analysis
- [ ] Machine learning predictions
- [ ] PDF report generation with charts
- [ ] API endpoint for programmatic access
- [ ] Docker containerization
- [ ] Cloud deployment (AWS, Azure, GCP)
- [ ] Data import from various sources (CSV, Excel, APIs)
- [ ] Custom dashboard builder

##  Support

For questions, issues, or suggestions:
- Contact via email : mabutsikgaogelo@gmail.com

##  Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- SQLAlchemy for elegant ORM
- The Python community
- [You can check it here](https://data-dashboard-ixwt7jzl8kpeknnseo5oga.streamlit.app/)

---

**Built with Love using Python and Streamlit**
