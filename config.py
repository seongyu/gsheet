import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# google sheet configuration
ENTER_SHEET = '1XjubDQaU3rk28RXhOZ8yVAH0gUpXVaOPp_G33wDox-4'
PROCESS_SHEET = '13-UduYjmLbOaq6NAgIbWXJemWSeWZ712XqN9TKKfe4A'
RELEASE_SHEET = '1J9BSeNatYRbNYSI3SmhIyrdBazDT6ZFRp0VSTHYMJJg'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'API Project'


def get_credentials():
  home_dir = os.path.expanduser('~')
  credential_dir = os.path.join(home_dir, '.credentials')
  if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
  credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
      flow.user_agent = APPLICATION_NAME
      credentials = tools.run_flow(flow, store, flags)
      print('Storing credentials to ' + credential_path)
  return credentials


# mysql configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PW = 'root1234'
DB_NAME = 'SMG'