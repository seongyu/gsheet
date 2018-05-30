# sheet_v2
# 
import lib.mysql as db


def compose_items(service,sheets):
  try :
    _upsert_ent(service,sheets['I'])
    _upsert_proc(service,sheets['P'])
  except Exception as err :
    print(err)
    pass
  return True

def upsert_log_data(service, sheets):
  arr = _get_from_ent(service, sheets['I'])
  arr.extend(_get_from_prc(service, sheets['P']))
  arr.extend(_get_from_rel(service, sheets['O']))

  return arr


def get_today_log(service, sheets, date_tag):
  arr = _get_today_data_enter(service, sheets['I'], date_tag)
  arr.extend(_get_today_data_proc(service, sheets['P'], date_tag))
  arr.extend(_get_today_data_rele(service, sheets['O'], date_tag))

  return arr

def _get_today_data_enter(service, sheet_id, date_tag):
  items = _get_enter_items(service, sheet_id)
  rangeName = '제품 부자재입고!N1:AAA'
  result = []
  arr = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='COLUMNS'
      ).execute().get('values',[])
  target_dt = [dt for dt in arr if  date_tag in dt]
  if len(target_dt) > 0:
   result = mk_upsert_item(target_dt, items)
  return result


def _get_today_data_proc(service, sheet_id, date_tag):
  items = _get_proc_items(service, sheet_id)
  rangeName = '납품처패키지작업현황!N1:AAA'
  result = []
  arr = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='COLUMNS'
      ).execute().get('values',[])
  target_dt = [dt for dt in arr if  date_tag in dt]
  if len(target_dt) > 0:
   result = mk_upsert_item(target_dt, items)
  return result


def _get_today_data_rele(service, sheet_id, date_tag):
  items = _get_rele_items(service, sheet_id)
  rangeName = '납품처 제품 출고!N1:AAA'
  result = []
  arr = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='COLUMNS'
      ).execute().get('values',[])
  target_dt = [dt for dt in arr if  date_tag in dt]
  if len(target_dt) > 0:
   result = mk_upsert_item(target_dt, items)
  return result






def _get_enter_items(service,sheet_id):
  items = []
  rangeName = '제품 부자재입고!C2:D'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  arr = request.execute().get('values',[])
  for ar in arr :
    item = {'type':'I'}
    item['main_code'] = ar[0]
    item['sub_code'] = ar[1]
    items.append(item)
  return items


def _get_proc_items(service,sheet_id):
  items = []
  rangeName = '납품처패키지작업현황!D2:E'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  arr = request.execute().get('values',[])
  for ar in arr :
    item = {'type':'P'}
    item['main_code'] = ar[0]
    item['sub_code'] = ar[1]
    items.append(item)
  return items


def _get_rele_items(service,sheet_id):
  items = []
  rangeName = '납품처 제품 출고!D2:E'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  arr = request.execute().get('values',[])
  for ar in arr :
    item = {'type':'O'}
    item['main_code'] = ar[0]
    item['sub_code'] = ar[1]
    items.append(item)
  return items


def _get_from_ent(service,sheet_id):
  items = _get_enter_items(service, sheet_id)

  rangeName = '제품 부자재입고!N1:AAA'
  arr = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='COLUMNS'
      ).execute().get('values',[])

  rearr = mk_upsert_item(arr,items)
  return rearr


def _get_from_prc(service,sheet_id):
  items = _get_proc_items(service, sheet_id)

  rangeName = '납품처패키지작업현황!N1:AAA'
  arr = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='COLUMNS'
      ).execute().get('values',[])

  rearr = mk_upsert_item(arr,items)
  return rearr

def _get_from_rel(service,sheet_id):
  items = _get_rele_items(service, sheet_id)

  rangeName = '납품처 제품 출고!N1:AAA'
  arr = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='COLUMNS'
      ).execute().get('values',[])

  rearr = mk_upsert_item(arr,items)
  return rearr


# compose array
def mk_upsert_item(arr,items):
  allItem = []
  for ar in arr :
    for i, a in enumerate(ar) :
      if a != '' and i != 0 :
        item = {'key':{},'value':{}}
        item['key'] = {
          'main_code' : items[i-1]['main_code'],
          'sub_code' : items[i-1]['sub_code'],
          'date_tag' : ar[0]
        }
        item['value'] = {
          'type' : items[i-1]['type'],
          'mount' : a  
        }
        allItem.append(item)
  return allItem


# def _get_types(str):
def get_enter_sheet(service,sheet_id):
  rangeName = '제품 부자재입고!A2:J'
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
    item['main_code'] = a[2]
    item['sub_code'] = a[3]
    item['company'] = a[0]
    item['type'] = a[4]
    item['total'] = a[9]
    items.append(item)

  return items

def get_process_sheet(service,sheet_id):
  rangeName = '납품처패키지작업현황!A2:K'
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
    item['main_code'] = a[3]
    item['sub_code'] = a[4]
    item['company'] = a[1]
    item['item'] = a[2]
    item['total'] = a[10]
    item['unfinish'] = a[7]
    items.append(item)

  return items

def get_release_sheet(service,sheet_id):
  rangeName = '납품처 제품 출고!A2:J'
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
    item['main_code'] = a[3]
    item['sub_code'] = a[4]
    item['company'] = a[1]
    item['vendor'] = a[0]
    item['item'] = a[2]
    item['total'] = a[9]
    item['stock'] = a[8]
    items.append(item)

  return items


def get_all_delevery_sheet(service,sheet_id):
  rangeName = '2018!A2:Q'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  t = request.execute().get('values',[])
  return t

def get_delevery_sheet(service,sheet_id, arr):
  rangeName = '2018!A2:Q'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  bt = request.execute().get('values',[])
  t = []
  for idx, it in enumerate(bt):
    if idx in arr :
      t.append(it)

  return t


def _upsert_ent(service, sheet_id):
  rangeName = '제품 부자재입고!A2:H'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  arr = request.execute().get('values',[])

  items = []
  for ar in arr :
    item = {'key':{},'value':{}}
    item['key']['main_code'] = ar[2]
    item['key']['sub_code'] = ar[3]
    item['value']['company_name'] = ar[0]
    item['value']['item_type'] = ar[4]
    item['value']['ea'] = ar[7]
    items.append(item)
  db.upsert(items, 'items')


def _upsert_proc(service, sheet_id):
  rangeName = '납품처패키지작업현황!A2:F'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName,
      majorDimension='ROWS'
      )
  arr = request.execute().get('values',[])

  items = []
  for ar in arr :
    item = {'key':{},'value':{}}
    item['key']['main_code'] = ar[3]
    item['key']['sub_code'] = ar[4]
    item['value']['item_name'] = ar[2]
    item['value']['target_name'] = ar[0]
    items.append(item)
  db.upsert(items, 'items')