# custom imports
import config
import db.mysql as db


def _enter_item(service,sheet_id):
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

  return db.insert('enter', items)

def _process_item(service,sheet_id):
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

  return db.insert('process', items)

def _release_item(service,sheet_id):
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

  return db.insert('sent', items)


def execute_enter(sheet_id):
  service = config.init()
  result = _enter_item(service, sheet_id)
  print(result)

def execute_process(sheet_id):
  service = config.init()
  result = _process_item(service, sheet_id)
  print(result)

def execute_release(sheet_id):
  service = config.init()
  result = _release_item(service, sheet_id)
  print(result)



# It would run 1 or 2 times every day
if __name__ == '__main__':
  execute_enter(config.ENTER_SHEET)
  execute_process(config.PROCESS_SHEET)
  execute_release(config.RELEASE_SHEET)


