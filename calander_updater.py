# calander_updater

# custom imports
import config
import db.mysql as db
import json
from datetime import datetime

f = '%m/%d/%Y %H:%M:%S'
## Total 17 column
#

def _get_from_sheet(service,sheet_id):
  rangeName = '2018!A2:Q'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  t = request.execute().get('values',[])

  items = []
  for a in t :
    item = {}
    item['po'] = a[5]
    item['company'] = a[4]
    item['description'] = a[7]
    item['product_type'] = a[1]
    item['type'] = a[2]
    item['status'] = a[3]
    item['unit'] = a[8]
    try :
      item['delevery'] = a[13].replace('\'','"')
    except :
      pass
    item['location'] = a[14]
    item['start_dt'] = datetime.strptime(a[15],f).strftime('%Y-%m-%d %H:%M:%S')
    item['end_dt'] = datetime.strptime(a[16],f).strftime('%Y-%m-%d %H:%M:%S')
    items.append(item)
  # return items
  return db.insert('delevery', items)

def get_sheet_data(sheet_id):
  service = config.init()
  try:
    _get_from_sheet(service, sheet_id)
    print('succssfully inserted..')
  except Exception as err :
    print('failed..',err)


if __name__ == '__main__':
  get_sheet_data(config.RESERVE_SHEET)