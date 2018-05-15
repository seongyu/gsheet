import config
import pymysql

arr = []

def _connect():
  db = pymysql.connect(
    config.DB_HOST,
    config.DB_USER,
    config.DB_PW,
    config.DB_NAME,
    charset='utf8')
  cursor = db.cursor()
  return (db, cursor)


## insert default items
# input
#  JsonArray
# output
#  result : boolean
def insert(table_name, dicts):
  (db, cursor) = _connect()
  d = {'result':True}
  try:
    for dic in dicts :
      placeholder = ", ".join(["%s"] * len(dic))
      stmt = "insert into {table} ({columns}) values ({values});".format(table=table_name, columns=",".join(dic.keys()), values=placeholder)
      cursor.execute(stmt, list(dic.values()))
  except Exception as err:
    print(err)
    db.rollback()
    d['result'] = False
  finally:
    db.commit()
    db.close()
    return d