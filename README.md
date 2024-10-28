Sales Forecasting Web Application
A Django-based web application for time series forecasting of sales data using Facebook Prophet.

Setup Instructions
Clone the repository:
git clone <repository-url>
cd sales_forecasting
Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install requirements:
pip install -r requirements.txt
Run migrations:
python manage.py migrate
Start the development server:
python manage.py runserver
Visit http://127.0.0.1:8000 in your web browser
Features
Time series forecasting using Facebook Prophet
Interactive web interface for selecting forecast period
Visualization of historical data and forecasts with confidence intervals
Bootstrap-based responsive design
Dataset
The application uses a sample sales dataset with daily sales records. The data is stored in CSV format with date and sales columns.

Model Details
The forecasting is performed using Facebook Prophet, which is particularly well-suited for time series data with:

Strong seasonal effects
Missing data
Outliers
Shifts in the trend
Challenges and Solutions
Data Preprocessing: Implemented proper date formatting and handling
Model Integration: Successfully integrated Prophet with Django
Visualization: Used Plotly for interactive charts
User Interface: Created a simple, intuitive interface using Bootstrap
