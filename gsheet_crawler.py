# custom imports
import config
import lib.mysql as db
import lib.sheet as sheet

from datetime import datetime

def execute_enter(sheet_id):
  service = config.init('sheet')
  result = sheet.get_enter_sheet(service, sheet_id)
  db.insert_many('enter', result)
  print('Successfully inserted : ','enter',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def execute_process(sheet_id):
  service = config.init('sheet')
  result = sheet.get_process_sheet(service, sheet_id)
  db.insert_many('process', result)
  print('Successfully inserted : ','process',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def execute_release(sheet_id):
  service = config.init('sheet')
  result = sheet.get_release_sheet(service, sheet_id)
  db.insert_many('sent', result)
  print('Successfully inserted : ','sent',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



# It would run 1 or 2 times every day
if __name__ == '__main__':
  execute_enter(config.ENTER_SHEET)
  execute_process(config.PROCESS_SHEET)
  execute_release(config.RELEASE_SHEET)


