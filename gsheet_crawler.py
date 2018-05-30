# custom imports
import config
import lib.mysql as db
import lib.sheet_v2 as sheet

from datetime import datetime

# def execute_enter(sheet_id):
#   service = config.init('sheet')
#   result = sheet.get_enter_sheet(service, sheet_id)
#   db.insert_many('enter', result)
#   print('Successfully inserted : ','enter',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# def execute_process(sheet_id):
#   service = config.init('sheet')
#   result = sheet.get_process_sheet(service, sheet_id)
#   db.insert_many('process', result)
#   print('Successfully inserted : ','process',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# def execute_release(sheet_id):
#   service = config.init('sheet')
#   result = sheet.get_release_sheet(service, sheet_id)
#   db.insert_many('sent', result)
#   print('Successfully inserted : ','sent',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



# # It would run 1 or 2 times every day
# if __name__ == '__main__':
#   execute_enter(config.ENTER_SHEET)
#   execute_process(config.PROCESS_SHEET)
#   execute_release(config.RELEASE_SHEET)


def update_all_column():
  service = config.init('sheet')

  sheets = {
    'I' : config.ENTER_SHEET,
    'P' : config.PROCESS_SHEET,
    'O' : config.RELEASE_SHEET
  }

  result = sheet.compose_items(service, sheets)
  if result :
    array = sheet.upsert_log_data(service, sheets)
  if len(array) > 0 :
    result = db.upsert(array,'manage_log')
  if result :
    print('successfully worked')
  else :
    print('does not work because of some problems')

def add_todays_status():
  service = config.init('sheet')

  sheets = {
    'I' : config.ENTER_SHEET,
    'P' : config.PROCESS_SHEET,
    'O' : config.RELEASE_SHEET
  }

  date_tag = datetime.today().strftime('%Y. %m. %d').replace('. 0','. ')
  # date_tag = '2018. 4. 27'
  array = sheet.get_today_log(service, sheets, date_tag)
  if len(array) > 0 :
    result = db.upsert(array, 'manage_log')

# add_todays_status()
# update_all_column()