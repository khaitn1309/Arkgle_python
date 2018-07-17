import sqlite3

def getRowValue(table,uid):
    conn = sqlite3.connect("../database.db")
    c = conn.cursor()
    listKey = c.execute('SELECT * FROM %s WHERE id = %i'
                        %(table,uid)).fetchone()
    conn.close()
    return listKey

def getColumnValue(column, table, uid):
    conn = sqlite3.connect("../database.db")
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    listKey = c.execute('SELECT %s FROM %s WHERE id = %i'
                        %(column,table,uid)).fetchall()
    conn.close()
    return listKey

def getCurrentUser():
    conn = sqlite3.connect("../database.db")
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    ls = c.execute('SELECT * FROM current_user').fetchall()
    uid = ls[0]
    conn.close()
    return uid



