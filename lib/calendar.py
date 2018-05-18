# calendar
# 

import config

service = config.init('calendar')

event = {
  'summary':'this is test',
  'description':'how are you doing? \n Im fine now',
  'start': {
    'dateTime':now,
    'timeZone':'Asia/Seoul'
    },
  'end':{
    'dateTime':now,
    'timeZone':'Asia/Seoul'
    }
  }

service.events().insert(calendarId='primary', body=event).execute()