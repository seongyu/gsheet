import httplib2
from apiclient import discovery
import re

# custom imports
import config

reg = '[a-zA-Z0-9-_]+'


# initailize google sheet service
def init():
  credentials = config.get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
  service = discovery.build('sheets','v4',http=http,discoveryServiceUrl=discoveryUrl)
  return service


# serialize entered item from sheet
def _serialize_enter_item(srevice,sheet_id):
  rangeName = '제품 부자재입고!A2:J'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  return request.execute().get('values',[])

def compose_item_info(t):
  item = {}
  for a in t :
    item['main_code'] = a[2]
    item['sub_code'] = a[3]
    item['type_name'] = a[4]
    item['company_name'] = a[0]
    item['enter_sum_count'] = a[9]



result = _serialize_enter_item(service,sheet_id)