
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Get the current date
today = datetime.today()

# Calculate the date 3 months ago
three_months_ago = today - relativedelta(months=1)

# Format the dates in YYYY-MM-DD format
today_str = today.strftime('%Y-%m-%d')
three_months_ago_str = three_months_ago.strftime('%Y-%m-%d')

START_DATE = three_months_ago_str
END_DATE = today_str
PROPERTY_ID = '368891428'   # Predicta account

# OAuth 2.0 credentials file location
CLIENT_SECRET_FILE = 'oauth/client_secret_predicta.json'
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly', 'https://www.googleapis.com/auth/webmasters.readonly']
SITE_URL = 'https://littlecheeks.com.au/'  

# SQL Server configuration
SQL_SERVER = ''
SQL_DATABASE = ''
SQL_USER = ''
SQL_PASSWORD = ''


# Path
USET_PATH_OAUTH = 'ga4_data/oauth/client_secret_predicta.json'

