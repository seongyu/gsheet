import httplib2
from apiclient import discovery
import re

#custom imports
import config

reg = '[a-zA-Z0-9-_]+'

def init():
  credentials = config.get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
  service = discovery.build('sheets','v4',http=http,discoveryServiceUrl=discoveryUrl)
  return service


# query line
def collect(srevice,sheet_id):
  rangeName = 'sheet1'
  request = service.spreadsheets(
    ).values(
    ).get(
      spreadsheetId=sheet_id,
      range=rangeName
      )

  return request.execute().get('values',[])


def update(service,sheet_id,data):
  rangeName = 'sheet2'
  value_input_option = 'USER_ENTERED'

  request = service.spreadsheets(
    ).values(
    ).update(
      spreadsheetId=sheet_id, 
      range=rangeName, 
      valueInputOption=value_input_option, 
      body={'values':data}
      )

  response = request.execute()
  return response

def insert(service,sheet_id,data):
  new_sheet = 'sheet3'
  value_input_option = 'USER_ENTERED'
  insert_data_option = 'INSERT_ROWS'
  is_error_occurred = False

  # create new sheet
  try : 
    service.spreadsheets(
      ).batchUpdate(
        spreadsheetId=sheet_id, 
        body={'requests':[{'addSheet':{'properties':{'title':new_sheet}}}]}
      ).execute()
  except Exception as err :
    print(err)
    is_error_occurred = True

  # input data
  if is_error_occurred == False :
    response = service.spreadsheets(
      ).values(
      ).update(
        spreadsheetId=sheet_id, 
        range=new_sheet, 
        valueInputOption=value_input_option, 
        body={'values':data}
        ).execute()

    return response



if __name__ == '__main__':
  # get gsheet id
  sheet_id = input('Insert sheet id : ')

  if bool(re.search(reg,sheet_id)) == False :
    sheet_id = '1qkEI5JDKg80g7pe2gkT6Y5SNbkrVOxMYjIXlJI-DW6Q'
    # print('you should insert Google Sheet ID. try again.')
    # exit(-1)

  # create service
  service = init()

  # Collect
  # input : Obj service, string sheet_id
  # output : JsonArray data
  result = collect(service,sheet_id)

  # Write
  # input : Obj service, string sheet_id, JsonArray data 
  # output : string result
  res = insert(service, sheet_id,result)

  print(res)