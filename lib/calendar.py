# calendar

import config, json
from datetime import datetime
import lib.mysql as db

import time

service = config.init('calendar')


def time_fix(timestring):
  return datetime.strptime(timestring,'%Y-%m-%d %H:%M:%S').isoformat()

def set_event(items, timestring, po, cal_id):
  fixed_time = time_fix(timestring)
  sub_str = ''
  for item in items:
    sub_str = sub_str + '{description} {unit} [{product_type}] [{type}] {status} \n '.format(
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
  if len(po) == 0 : po = '등록하지 않은 PO'
  event = {'summary':po, 'description':sub_str, 'start':start, 'end':start}
  if len(cal_id) > 0 :
    result = service.events().patch(calendarId='primary', eventId=cal_id, body=event).execute()
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





