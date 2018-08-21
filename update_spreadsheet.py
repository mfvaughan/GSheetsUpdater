from __future__ import print_function
from pprint import pprint
from googleapiclient import discovery
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
from helpers import col_string
from credentials import SPREADSHEET_ID, TEST_DATA

# Credentials & stuff
SCOPES =  ['https://www.googleapis.com/auth/drive',
     'https://www.googleapis.com/auth/drive.file',
     'https://www.googleapis.com/auth/spreadsheets']

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = discovery.build('sheets', 'v4', credentials=creds)

def update_gsheet_data(worksheet, data, data_range=None):
    # Test data
    if type(data) is list:
        values = data
        RANGE_END_CHAR = len(values[0]) # Based on the # of columns of data
        RANGE_END_INT = len(values[1:]) # Based on the number of rows of data 
    else:
        df = pd.read_csv(data)
        data_cols, data_values = df.columns.tolist(), df.values.tolist()
        values = ([data_cols] + data_values)
        RANGE_END_CHAR = col_string(len(data_cols)) # Based on the # of columns of data
        RANGE_END_INT = len(values) # Based on the number of rows of data

    # Some more variables ...
    SHEET_NAME = ''
    RANGE_START = 'A1' # Always start at A1
    VALUE_INPUT_OPTION = 'USER_ENTERED'
    if data_range is None:
        RANGE = '{}!{}:{}{}'.format(SHEET_NAME, RANGE_START, RANGE_END_CHAR, RANGE_END_INT)
    else:
        RANGE = data_range

    # Build the request ...
    data = [
        {
            'values': values,
            'range': RANGE
        }
    ]

    body = {
    'valueInputOption': VALUE_INPUT_OPTION,
    'data': data
    }

    result = service.spreadsheets().values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body)
    response = result.execute()
    pprint(response)
    
    return response
    
if __name__ == "__main__":   
    update_gsheet_data(SPREADSHEET_ID, TEST_DATA)