#custom imports
import config, json
from flask import Flask, request
import lib.mysql as db
import calendar_updater as cu

app = Flask(__name__)

@app.route('/u',methods=['post'])
def get_data():
  data = request.form['rows'] # [1,2,3,4]  
  return response(data)

@app.route('/ua',methods=['post'])
def get_data():
  cu.get_sheet_data(config.RESERVE_SHEET)
  return response('')

def response(data):
  res = {'status':'OK','data':data}
  return json.dumps(res)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8080')