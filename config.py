import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
from apiclient.discovery import build
import re

# google sheet configuration
ENTER_SHEET = '1XjubDQaU3rk28RXhOZ8yVAH0gUpXVaOPp_G33wDox-4'
PROCESS_SHEET = '13-UduYjmLbOaq6NAgIbWXJemWSeWZ712XqN9TKKfe4A'
RELEASE_SHEET = '1J9BSeNatYRbNYSI3SmhIyrdBazDT6ZFRp0VSTHYMJJg'
RESERVE_SHEET = '1dp6EfdXMHbkqp7CuZmaXpVZuopEMbH9XeaEIGBoVylk'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

GSHEET_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
GSHEET_CLIENT_SECRET_FILE = 'client_secret.gsheet.json'
CALENDER_SCOPES = 'https://www.googleapis.com/auth/calendar'
CALENDER_CLIENT_SECRET_FILE = 'client_secret.calender.json'
APPLICATION_NAME = 'API Project'

# initailize google calendar service
def init(service_name):
  home_dir = os.path.expanduser('~')
  credential_dir = os.path.join(home_dir, '.credentials')
  if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

  if service_name=='sheet':
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
  elif service_name=='calendar':
    credential_path = os.path.join(credential_dir, 'calender.googleapis.com-python-quickstart.json')
  else :
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:

    if service_name=='sheet':
      flow = client.flow_from_clientsecrets(GSHEET_CLIENT_SECRET_FILE, GSHEET_SCOPES)
    elif service_name=='calendar':
      flow = client.flow_from_clientsecrets(CALENDER_CLIENT_SECRET_FILE, CALENDER_SCOPES)
    else :
      flow = client.flow_from_clientsecrets(GSHEET_CLIENT_SECRET_FILE, GSHEET_SCOPES)

    flow.user_agent = APPLICATION_NAME
    credentials = tools.run_flow(flow, store, flags)

  discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
  if service_name=='sheet':
    service = build('sheets', 'v4', http=credentials.authorize(httplib2.Http()), discoveryServiceUrl=discoveryUrl)
  elif service_name=='calendar':
    service = build('calendar', 'v3', http=credentials.authorize(httplib2.Http()))
  else :
    service = build('sheets', 'v4', http=credentials.authorize(httplib2.Http()), discoveryServiceUrl=discoveryUrl)

  return service

# mysql configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PW = 'root1234'
DB_NAME = 'SMG'