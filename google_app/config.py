
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR


PROPERTY_ID = '368891428'   # Predicta account
START_DATE = '30daysAgo'
END_DATE = 'today'

# OAuth 2.0 credentials file location
CLIENT_SECRET_FILE_ROOT = 'Code/oauth/'
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

# SQL Server configuration
SQL_SERVER = ''
SQL_DATABASE = ''
SQL_USER = ''
SQL_PASSWORD = ''

# Path
USET_PATH_OAUTH = os.path.join(BASE_DIR, 'oauth', 'client_secret_predicta.json')

