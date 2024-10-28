# Sales Forecasting Web Application

A dual-implementation sales forecasting application using both Django and Streamlit, providing flexible options for deployment and visualization.

## Django Implementation
A Django-based web application for time series forecasting of sales data using Facebook Prophet.

### Setup Instructions (Django)
1. Clone the repository:
```bash
git clone <repository-url>
cd sales_forecasting
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Visit http://127.0.0.1:8000 in your web browser

### Features (Django)
* Time series forecasting using Facebook Prophet
* Interactive web interface for selecting forecast period
* Visualization of historical data and forecasts with confidence intervals
* Bootstrap-based responsive design

## Streamlit Implementation
A Streamlit-based version offering enhanced data visualization and easier deployment options.

### Setup Instructions (Streamlit)
1. Ensure you're in the project directory and virtual environment is activated
2. Install Streamlit-specific requirements:
```bash
pip install streamlit pandas plotly prophet
```

3. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

4. The application will automatically open in your default web browser

### Features (Streamlit)
* **Enhanced Interactive Dashboard:**
  - Real-time forecast updates
  - Interactive date range selection
  - Dynamic store and department filtering
  - Responsive layout adaptation

* **Advanced Visualization:**
  - Interactive Plotly charts
  - Confidence interval visualization
  - Trend analysis display
  - Forecast summary tables

* **User Interface Components:**
  - Sidebar for parameter selection
  - Multiple metric displays
  - Data filtering options
  - Interactive chart controls

* **Data Analysis Features:**
  - Store-specific analysis
  - Department-level forecasting
  - Weekly sales patterns
  - Holiday effect analysis

### Why Streamlit?
* **Rapid Development:**
  - Faster implementation of data science applications
  - Less boilerplate code compared to Django
  - Built-in support for data science libraries

* **Enhanced Visualization:**
  - Native support for various plotting libraries
  - Interactive charts and graphs
  - Real-time updates without page refreshes

* **User Experience:**
  - More intuitive interface for data science applications
  - Easier navigation for data analysis tasks
  - Better handling of large datasets

* **Deployment Simplicity:**
  - Easier deployment process
  - Built-in caching mechanisms
  - Simple configuration options

## Dataset
The application uses a sample sales dataset with the following structure:
* Store: Store identifier
* Department: Department identifier
* Date: Sales date
* Weekly_Sales: Sales amount
* IsHoliday: Holiday flag

## Model Details
The forecasting is performed using Facebook Prophet, which is particularly well-suited for time series data with:
* Strong seasonal effects
* Missing data
* Outliers
* Shifts in the trend

## Implementation Comparison

| Feature | Django | Streamlit |
|---------|--------|-----------|
| Setup Complexity | Higher | Lower |
| Development Time | Longer | Shorter |
| Customization | More Flexible | Limited to Data Apps |
| Visualization | Basic | Advanced |
| Learning Curve | Steeper | Gentler |
| Best For | Full Web Apps | Data Applications |

## Technical Requirements
* Python 3.7+
* Required packages:
  - Django (for web framework)
  - Streamlit (for data app)
  - Prophet (for forecasting)
  - Plotly (for visualization)
  - Pandas (for data manipulation)
  - NumPy (for numerical operations)

## Future Improvements
* Integration of additional forecasting models
* Enhanced data preprocessing options
* More advanced visualization features
* API endpoint development
* Extended documentation

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
