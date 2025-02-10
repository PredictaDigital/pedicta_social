

import os
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy import inspect
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import pickle
import pandas as pd
from .config import *



def check_and_refresh_token(creds):
    """Check and refresh token if necessary"""
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def get_credentials():
    """Authenticate and return the Google Search Console API client."""
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

    try:
        service = build('searchconsole', 'v1', credentials=creds)
        return service, creds
    except Exception as err:
        print(f'Error occurred: {err}')
        return None

def extract_GSC_webpage_data(service, site_url):
    """Fetch Google Search Console data for the given site URL."""
    try:
        print('Extracting data ...')

        # Define the request parameters (e.g., top 100 queries, impressions, clicks, CTR, etc.)
        request = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                'startDate': '2024-01-01',  # Change to your desired start date
                'endDate': '2024-01-31',  # Change to your desired end date
                'dimensions': ['query', 'page', 'country', 'device'],
                'rowLimit': 1000  # Increase if needed
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
                'startDate': '2024-01-01',  # Keep same as requested date range
                'endDate': '2024-01-31',    # Keep same as requested date range
                'aggregationType': 'TOTAL',  # Assuming 'TOTAL', adjust if needed
                'country': row.get('keys', [None])[1],  # Country is the second key
                'device': row.get('keys', [None])[2],  # Device is the third key
                'page': row.get('keys', [None])[0],    # Page is the first key
                'query': row.get('keys', [None])[0],   # Query is the first key
                'date': '2024-01-01',  # Date as a placeholder, adjust if you need daily data
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
    table_name = f"GSC_Test_{table_name}"
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

def load_data_to_excel_file(data_df, f_name):
    data_df.to_excel(f'GSC_Test_{f_name}.xlsx',index=False)

