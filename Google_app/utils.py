




import os
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy import inspect
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import pickle
import pandas as pd
from .config import *


def get_credentials():
    """Handles OAuth 2.0 authentication flow and token refresh"""
    creds = None
    # The token.pickle file stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there is no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)  
            creds = flow.run_local_server(port=8001)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_google_service(creds):
    """ Create required the service for Google Search Console """
    try:
        service = build('searchconsole', 'v1', credentials=creds)
        return service
    except Exception as err:
        print(f'Error occurred: {err}')
        return None

def check_and_refresh_token(creds):
    """Check and refresh token if necessary"""
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def extract_GA4_session_data(creds):
    """ Extract data to create GA4_seession table """

    client = BetaAnalyticsDataClient(credentials=creds)

    # https://stackoverflow.com/questions/66853674/number-of-dimensions-allowed-in-ga4-data-api
    request = {
        "property": f"properties/{PROPERTY_ID}",
        "date_ranges": [DateRange(start_date = START_DATE, end_date = END_DATE)],
        "dimensions": [
            Dimension(name="date"),
            Dimension(name="cityId"),
            Dimension(name="city"),
            Dimension(name="deviceCategory"),
            Dimension(name="firstUserSourceMedium"),
            Dimension(name="sessionSource")],
        "metrics": [
            Metric(name="sessions"),
            Metric(name="activeusers"),
            Metric(name="newUsers"),
            Metric(name="totalUsers"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="eventCount"),
            Metric(name="conversions"),
            Metric(name="screenPageViews")],
    }
    
    response = client.run_report(request)

    data = []
    for row in response.rows:
        data.append({
            "date": row.dimension_values[0].value,
            "city": row.dimension_values[1].value,
            "deviceCategory": row.dimension_values[2].value,
            "firstUserSourceMedium": row.dimension_values[3].value,
            "sessionSource": row.dimension_values[4].value,

            "sessions": row.metric_values[0].value,
            "activeusers": row.metric_values[1].value,
            "newUsers": row.metric_values[2].value,
            "totalUsers": row.metric_values[3].value,
            "bounceRate": row.metric_values[4].value,
            "averageSessionDuration": row.metric_values[5].value,
            "eventCount": row.metric_values[6].value,
            "conversions": row.metric_values[7].value,
            "screenPageViews": row.metric_values[8].value
        })
    
    return pd.DataFrame(data)

def extract_GA4_event_data(creds):
    """ Extract data to create GA4_Event table """

    client = BetaAnalyticsDataClient(credentials=creds)
    request = {
        "property": f"properties/{PROPERTY_ID}",
        "date_ranges": [DateRange(start_date = START_DATE, end_date = END_DATE)],
        "dimensions": [
            Dimension(name="date"),
            Dimension(name="cityId"),
            Dimension(name="city"),
            Dimension(name="deviceCategory"),
            Dimension(name="firstUserSourceMedium"),
            Dimension(name="sessionSource"),
            Dimension(name="pagePath"),
            Dimension(name="pageTitle"),
            Dimension(name="eventName"),
            ],
        "metrics": [
            Metric(name="sessions"),
            Metric(name="activeusers"),
            Metric(name="newUsers"),
            Metric(name="totalUsers"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="eventCount"),
            Metric(name="conversions"),
            Metric(name="screenPageViews")],
    }
    
    response = client.run_report(request)

    data = []
    for row in response.rows:
        data.append({
            "date": row.dimension_values[0].value,
            "city": row.dimension_values[1].value,
            "deviceCategory": row.dimension_values[2].value,
            "firstUserSourceMedium": row.dimension_values[3].value,
            "sessionSource": row.dimension_values[4].value,
            "pagePath": row.dimension_values[5].value,
            "pageTitle": row.dimension_values[6].value,
            "eventName": row.dimension_values[7].value,

            "sessions": row.metric_values[0].value,
            "activeusers": row.metric_values[1].value,
            "newUsers": row.metric_values[2].value,
            "totalUsers": row.metric_values[3].value,
            "bounceRate": row.metric_values[4].value,
            "averageSessionDuration": row.metric_values[5].value,
            "eventCount": row.metric_values[6].value,
            "conversions": row.metric_values[7].value,
            "screenPageViews": row.metric_values[8].value
        })
    
    return pd.DataFrame(data)

def extract_GA4_webpage_data(creds):
    """ Extract data to create GA4_Web_Page table """

    client = BetaAnalyticsDataClient(credentials=creds)
    request_part1 = {
        "property": f"properties/{PROPERTY_ID}",
        "date_ranges": [DateRange(start_date = START_DATE, end_date = END_DATE)],
        "dimensions": [
            Dimension(name="date"),
            Dimension(name="country"),
            Dimension(name="cityId"),
            Dimension(name="city"),
            Dimension(name="deviceCategory"),
            Dimension(name="pagePath"),
            Dimension(name="pagePathPlusQueryString"),
            Dimension(name="pageTitle")
            ]
    }
    
    response_part1 = client.run_report(request_part1)
    data = []
    for row in response_part1.rows:
        data.append({
            "date": row.dimension_values[0].value,
            "country": row.dimension_values[1].value,
            "cityId": row.dimension_values[2].value,
            "city": row.dimension_values[3].value,
            "deviceCategory": row.dimension_values[4].value,
            "pagePath": row.dimension_values[5].value,
            "pagePathPlusQueryString": row.dimension_values[6].value,
            "pageTitle": row.dimension_values[7].value,
            "startDate": START_DATE,
            "endDate": END_DATE,
        })

    return pd.DataFrame(data)

def extract_GSC_webpage_data(service, site_url):
    """Fetch Google Search Console data for the given site URL."""
    try:
        print('Extracting data ...')
        # Define the request parameters
        request = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                'startDate': START_DATE,  
                'endDate': END_DATE,  
                'dimensions': ['query', 'page', 'country', 'device']
            }
        )        
        response = request.execute()
        
        # Extract the relevant data
        data = []
        for row in response.get('rows', []):
            data.append({
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0),
                'position': row.get('position', 0),
                'site_url': site_url,
                'startDate': START_DATE,                # Keep same as requested date range
                'endDate': END_DATE,                    # Keep same as requested date range
                'aggregationType': 'TOTAL',             # Assuming 'TOTAL', adjust if needed
                'country': row.get('keys', [None])[1],  # Country is the second key
                'device': row.get('keys', [None])[2],   # Device is the third key
                'page': row.get('keys', [None])[0],     # Page is the first key
                'query': row.get('keys', [None])[0],    # Query is the first key
                'date': START_DATE,                     # Date as a placeholder, adjust if you need daily data
            })
        
        return pd.DataFrame(data)
    except Exception as err:
        print(f'Error occurred: {err}')
        return []

def insert_data_to_db(df, table_name):
    """ create a table and insert data to SQL database """

    # Create the SQLAlchemy engine
    engine = create_engine(
        f"mssql+pyodbc://{SQL_USER}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    table_name = f"GA4_Test_{table_name}"
    metadata = MetaData()
    conn = engine.connect()

    # Define the table dynamically based on DataFrame columns
    table = Table(
        table_name,
        metadata,
        *(Column(col, String, nullable=True) for col in df.columns)
    )

    insp = inspect(engine)
    # Create the table if it doesn't exist
    if not insp.has_table(table_name):
        metadata.create_all(engine, tables=[table])

    # Insert DataFrame data into the table
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Data inserted into table '{table_name}'.")

    conn.close()

def load_data_to_excel_file(data, f_name):
    pd.DataFrame(data).to_excel(f'GA4_Test_{f_name}.xlsx',index=False)

