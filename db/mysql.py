import config

import pymysql

db = pymysql.connect(config.DB_HOST,config.DB_USER,config.DB_PW,config.DB_NAME)
