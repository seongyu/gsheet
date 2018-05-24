# sheet

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