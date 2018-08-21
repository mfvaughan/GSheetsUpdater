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

# Test data
df = pd.read_csv(TEST_DATA)
df_cols, df_data = df.columns.tolist(), df.values.tolist()
values = ([df_cols] + df_data)

# Some variables ...
RANGE_START = 'A1' # Always start at A1
RANGE_END_CHAR = col_string(len(df_cols)) # Based on the # of columns of data
RANGE_END_INT = len(values) # Based on the number of rows of data
VALUE_INPUT_OPTION = 'USER_ENTERED'

# Build the request ...
data = [
    {
        'values': values,
        'range': '{}:{}{}'.format(RANGE_START, RANGE_END_CHAR, RANGE_END_INT)
    }
]

body = {
  'valueInputOption': VALUE_INPUT_OPTION,
  'data': data
}

result = service.spreadsheets().values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body)
response = result.execute()
pprint(response)