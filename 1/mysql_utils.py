#coding: utf-8

import MySQLdb
import sae.const

def conn_open():
    db = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                         user=sae.const.MYSQL_USER,
                         passwd=sae.const.MYSQL_PASS,
                         db=sae.const.MYSQL_DB,
                         port=int(sae.const.MYSQL_PORT))
    return db    


def get_info_from_db(s_sql):
    db = conn_open()
    cursor = db.cursor()
    cursor.execute(s_sql)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows

