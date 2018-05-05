import re
reg = '[a-zA-Z0-9-_]+'

sheet_id = input('Insert sheet id : ')

if bool(re.search(reg,sheet_id)) == False :
  sheet_id = '1qkEI5JDKg80g7pe2gkT6Y5SNbkrVOxMYjIXlJI-DW6Q'
  # print('you should insert Google Sheet ID. try again.')
  # exit(-1)

url = 'https://docs.google.com/spreadsheets/d/'+sheet_id+'/edit#gid=0'

