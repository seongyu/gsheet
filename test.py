#custom imports
import config, json
from flask import Flask, request
import lib.mysql as db
#import lib.calendar as calendar


def testFn():
  (db, cursor) = _connect()
  stmt = 'select * from test;';
  cursor.execute(stmt)
  rows = cursor.fetchall()
  db.close()

app = Flask(__name__)

@app.route('/',methods=['post'])
def get_data():
  data = request.form
  return response(data)


def response(data):
  res = {'status':'OK','data':data}
  return json.dumps(res)


if __name__ == '__main__':
  testFn()
  app.run(host='0.0.0.0', port='5000')