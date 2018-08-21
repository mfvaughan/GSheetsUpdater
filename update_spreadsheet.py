from __future__ import print_function
from pprint import pprint
from googleapiclient import discovery
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
from helpers import col_string

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
df = pd.read_csv(r"C:\Users\MV\Documents\Code\g_sheets\test.csv")
df_cols, df_data = df.columns.tolist(), df.values.tolist()
values = ([df_cols] + df_data)

# Some variables ...
SPREADSHET_ID = '1S-5IU1Lb14EztrHewwW4e2Ymht_VpPwBAq-IFmeUYN8'
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

result = service.spreadsheets().values().batchUpdate(spreadsheetId=SPREADSHET_ID, body=body)
response = result.execute()
pprint(response)