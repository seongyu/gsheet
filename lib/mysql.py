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
def insert_many(table_name, dicts):
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

# insert update
def calendar_triger(items, dt, po):
  cal_udt = []
  db_name = 'delevery'
  (db, cursor) = _connect()
  stmt = 'select * from {db_name} where po={po} and start_dt={dt};'.format(db_name=db_name, po=po, dt=dt)
  cursor.execute(stmt)
  rows = cursor.fetchall()
  db.close()
  for_triger = {'is':False,'calendar_id':''}
  for item in items:
    # 같은 description이 있을때
    if len([row for row in rows if item['description'] item]) > 0:
      # 데이터가 다를 경우
      if len([row for row in rows if
       row[4]==item['product_type'] and 
       row[5]==item['type'] and 
       row[6]==item['status'] and 
       row[7]==item['unit'] and 
       row[8]==item['delevery']]) == 0 :
        _update('delevery', item, row[0])
        # if row[13] and not row[13] in cal_udt : cal_udt.append(row[13])
        if row[13] : 
          for_triger['is'] = True
          for_triger['calendar_id'] = row[13]
        else :
          for_triger['is'] = True
      # 데이터가 같을경우 : pass
    # 같은 description이 없을때
    else :
      _insert('delevery', item)
      for_triger['is'] = True
  return for_triger

# insert single
def _insert(table_name, dic):
  (db, cursor) = _connect()
  placeholder = ", ".join(["%s"] * len(dic))
  stmt = "insert into {table} ({columns}) values ({values});".format(table=table_name, columns=",".join(dic.keys()), values=placeholder)
  try:
    cursor.execute(stmt, list(dic.values()))
    db.commit()
  except:
    db.rollback()
  finally:
    db.close()

# update single
def _update(table_name, dic, idx):
  (db, cursor) = _connect()
  stmt = "update {table} set product_type=%s, type=%s, status=%s, unit=%s, delevery=%s where idx={idx};".format(table=table_name, idx=idx)
  try:
    cursor.execute(stmt, (dic['product_type'],dic['type'],dic['status'],dic['unit'],dic['delevery']))
    db.commit()
  except:
    db.rollback()
  finally:
    db.close()







