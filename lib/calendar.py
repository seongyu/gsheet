# calendar

import config, json
from datetime import datetime
import lib.mysql as db

import time

service = config.init('calendar')


def time_fix(timestring):
  return datetime.strptime(timestring,'%Y-%m-%d %H:%M:%S').isoformat()

def set_event(items, timestring, po, triger):
  fixed_time = time_fix(timestring)
  sub_str = ''
  for item in items:
    sub_str = sub_str + '{description} {unit} {status} \n '.format(
      description=item['description'], 
      product_type=item['product_type'], 
      type=item['type'],
      status=item['status'], 
      unit=item['unit'])
    try :
      delevery = json.loads(item['delevery'])
      for ar in delevery.keys():
        sub_str = sub_str + ar + ' ' + str(delevery[ar]) + ' \n '
    except Exception as err :
      print(err)
  start = {
    'dateTime' : fixed_time,
    'timeZone':'Asia/Seoul'
  }
  if len(po) == 0 : triger['description'] = '등록하지 않은 PO'

  summary = '[{product_type}|{type}] {description}'.format(product_type=triger['product_type'], type=triger['type'], description=triger['description'])
  if triger['type']== '납품':
    summary = 'N' + summary
  elif triger['type']== '입고':
    summary = 'I' + summary
  elif triger['type']== '반출':
    summary = 'B' + summary
      
  event = {'summary':summary, 'description':sub_str, 'start':start, 'end':start}
  if len(triger['calendar_id']) > 0 :
    result = service.events().patch(calendarId='primary', eventId=triger['calendar_id'], body=event).execute()
    print('udt >>',result['id'])
  else :  
    result = service.events().insert(calendarId='primary', body=event).execute()
    print('add >>',result['id'])
  return result

def test_set_event():
  now = {
    'dateTime':datetime.utcnow().isoformat(),
    'timeZone':'Asia/Seoul'
  }
  event = {'summary':'test title', 'description':'test_event', 'start':now, 'end':now}
  result = service.events().insert(calendarId='primary', body=event).execute()
  print(result['id'])
  time.sleep(5)
  event['summary'] = 'renamed title'
  service.events().patch(calendarId='primary', eventId=result['id'], body=event).execute()
  print(result['id'])





