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
  stmt = 'select * from {db_name} where po="{po}" and start_dt="{dt}";'.format(db_name=db_name, po=po, dt=dt)
  cursor.execute(stmt)
  rows = cursor.fetchall()
  db.close()

  for_triger = {'is':False,'calendar_id':''}
  for item in items:
    # 같은 description이 있을때
    if len([row for row in rows if item['description'] in row]) > 0:
      # 데이터가 다를 경우
      if len([row for row in rows if row[7]==item['unit'] and row[8]==item['delevery']]) == 0 :
        row = rows[0]
        cal_update('delevery', item, row[0])
        # if row[13] and not row[13] in cal_udt : cal_udt.append(row[13])
        if row[13] and len(row[13]) > 0 : 
          for_triger['is'] = True
          for_triger['calendar_id'] = row[13]
          for_triger['description'] = row[3]
          for_triger['product_type'] = row[4]
          for_triger['type'] = row[5]
        # 캘린더 ID가 없는경우
        else :
          for_triger['is'] = True
          for_triger['description'] = row[3]
          for_triger['product_type'] = row[4]
          for_triger['type'] = row[5]
      # 데이터가 같을경우 : pass
      # else:
      #   row = [row for row in rows if item['description'] in row][0]
      #   if row[13] and len(row[13]) > 0 : 
      #     for_triger['calendar_id'] = row[13]
    # 같은 description이 없을때
    else :
      cal_insert('delevery', item)
      for_triger['is'] = True
      for_triger['description'] = item['description']
      for_triger['product_type'] = item['product_type']
      for_triger['type'] = item['type']

  return for_triger

# insert single
def cal_insert(table_name, dic):
  # return None
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
def cal_update(table_name, dic, idx):
  # return None
  (db, cursor) = _connect()
  stmt = "update {table} set product_type=%s, type=%s, status=%s, unit=%s, delevery=%s where idx={idx};".format(table=table_name, idx=idx)
  try:
    cursor.execute(stmt, (dic['product_type'],dic['type'],dic['status'],dic['unit'],dic['delevery']))
    db.commit()
  except:
    db.rollback()
  finally:
    db.close()

# update calendar_id
def calendar_id_update(po, start_dt, calendar_id):
  (db, cursor) = _connect()
  stmt = "update delevery set calendar_id=%s where po=%s and start_dt=%s;"
  try:
    cursor.execute(stmt,(calendar_id, po, start_dt))
    db.commit()
  except:
    db.rollback()
  finally:
    db.close()


def testFn():
  (db, cursor) = _connect()
  stmt = 'select * from test;';
  cursor.execute(stmt)
  rows = cursor.fetchall()
  db.close()
  print(rows)

# array {values .... , keys .... }
def upsert(arr,table_name):
  (db, cursor) = _connect()
  result = True
  try :
    for ar in arr :
      if table_name == 'items':
        stmt = 'select * from {table_name} where main_code = %s and sub_code = %s;'.format(table_name=table_name)
      else :
        stmt = 'select * from {table_name} where main_code = %s and sub_code = %s and date_tag = %s;'.format(table_name=table_name)
      cursor.execute(stmt, list(ar['key'].values()) )
      rows = cursor.fetchall()
      if len(rows) > 0 : # update
        _update(db, cursor, table_name, ar['value'], ar['key'])
      else :
        for a in list(ar['key'].keys()):
          ar['value'][a] = ar['key'][a]
        _insert(db,cursor,table_name, ar['value'])
    db.commit()
  except Exception as err:
    print(err)
    db.rollback()
    result = False
  finally:
    db.close()
  return result



# insert single
def _insert(db, cursor, table_name, dic):
  placeholder = ", ".join(["%s"] * len(dic))
  stmt = "insert into {table} ({columns}) values ({values});".format(table=table_name, columns=",".join(dic.keys()), values=placeholder)
  cursor.execute(stmt, list(dic.values()))

# update single
def _update(db, cursor, table_name, dic, key):
  columns = []
  for d in list(dic.keys()) :
    if len([k for k in key.keys() if d in k]) <= 0:
      columns.append(d+'=%s')

  keys = []
  for d in list(key.keys()) :
    keys.append(d+'=%s')
    dic[d] = key[d]

  stmt = "update {table} set {columns} where {keys};".format(table=table_name, columns=",".join(columns), keys=" and ".join(keys))
  cursor.execute(stmt, list(dic.values()))


