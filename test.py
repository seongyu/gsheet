#custom imports
import config, json
from flask import Flask, request
import lib.mysql as db
#import lib.calendar as calendar

app = Flask(__name__)

@app.route('/',methods=['post'])
def get_data():
  data = request.form
  print(data)
  return response(data)


def response(data):
  res = {'status':'OK','data':data}
  return json.dumps(res)


if __name__ == '__main__':
  # db.testFn()
  app.run(host='0.0.0.0', port='8080')