# calendar_updater

# custom imports
import config
import lib.mysql as db
import lib.calendar as cal
import lib.sheet as sheet
import json
from datetime import datetime

f = '%m/%d/%Y %H:%M:%S'
## Total 17 column

def _grouping(arr):
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  items = {}
  for a in arr :
    item = {}
    item['start_dt'] = datetime.strptime(a[15],f).strftime('%Y-%m-%d %H:%M:%S')
    if True :
    # if item['start_dt'] > now :
      items = _arr_crt(items, item['start_dt'], False)
      item['end_dt'] = datetime.strptime(a[16],f).strftime('%Y-%m-%d %H:%M:%S')
      item['po'] = a[5]
      items[item['start_dt']] = _arr_crt(items[item['start_dt']], item['po'], True)
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

      items[item['start_dt']][item['po']].append(item)
  return items

## check JsonObj and create key
# obj = {}, key = 'string' , is_arr = boolean
# 
def _arr_crt(obj, key, is_arr):
  if key not in obj :
    if is_arr :
      obj[key] = []
    else :
      obj[key] = {}
  return obj

# def _get_from_sheet(service,sheet_id):
#   rangeName = '2018!A2:Q'
#   request = service.spreadsheets(
#     ).values(
#     ).get(
#       spreadsheetId=sheet_id,
#       range=rangeName,
#       majorDimension='ROWS'
#       )
#   t = request.execute().get('values',[])

#   items = []
#   for a in t :
#     item = {}
#     item['po'] = a[5]
#     item['company'] = a[4]
#     item['description'] = a[7]
#     item['product_type'] = a[1]
#     item['type'] = a[2]
#     item['status'] = a[3]
#     item['unit'] = a[8]
#     try :
#       item['delevery'] = a[13].replace('\'','"')
#     except :
#       pass
#     item['location'] = a[14]
#     item['start_dt'] = datetime.strptime(a[15],f).strftime('%Y-%m-%d %H:%M:%S')
#     item['end_dt'] = datetime.strptime(a[16],f).strftime('%Y-%m-%d %H:%M:%S')
#     items.append(item)
#   # return items
#   return db.insert('delevery', items)

def _db_procedure(items):
  for dt_item in items :
    for po_item in items[dt_item]:
      for_triger = db.calendar_triger(items[dt_item][po_item], dt_item, po_item)
      # print(for_triger)
    #if for_triger['is'] :
      result = cal.set_event(items[dt_item][po_item], dt_item, po_item, for_triger)
      if len(result['id']) > 0 and len(for_triger['calendar_id']) == 0 :
        db.calendar_id_update(po_item, dt_item, result['id'])
  print('Done...')
    
def get_sheet_data(sheet_id):
  print(sheet_id)
  service = config.init('sheet')
  try:
    t = sheet.get_delevery_sheet(service, sheet_id)
    r = _grouping(t)
    print('succssfully gettering from sheet..')
  except Exception as err :
    print('failed..',err)
    r = []
  if len(r) > 0 :
    _db_procedure(r)


if __name__ == '__main__':
  get_sheet_data(config.RESERVE_SHEET)