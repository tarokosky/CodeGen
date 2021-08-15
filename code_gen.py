#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import random
import sqlite3
import time

code_db_path = 'code.db'

def code_gen(size=6):
    print("Generating code ... ")

    key_chars=string.digits
    value_chars=string.ascii_uppercase

    code = ''.join(random.choice(key_chars) for _ in range(size))
    value = ''.join(random.choice(value_chars) for _ in range(size))
    timestamp = time.monotonic_ns()
    insert_db_sq3(code_db_path, code, value, timestamp)
    #insert_db_sq3(":memory:", code, value, timestamp)

    return code, value, timestamp

def code_verify(code):
    print("Verifying code ... ")
    value = query_db(code_db_path, code)
    return value

def insert_db_sq3(db_path, code, value, timestamp):
    #print("Insert to sq3 DB")
    #con = sqlite3.connect( code_db_path )
    con = sqlite3.connect( db_path )
    cur = con.cursor()
    sql_cmd = 'CREATE TABLE IF NOT EXISTS code_table ( CODE_ID INTEGER PRIMARY KEY ASC ,code TEXT, value TEXT, timestamp timestamp, expired BLOB)'
    try:
        cur.execute( sql_cmd )
    except:
        print("Create table error")


    sql_cmd = "INSERT INTO code_table ( code, value, timestamp )VALUES ( ?, ?, ? )"
    #print("sql_cmd = %s" % sql_cmd)
    try:
        cur.execute( sql_cmd, [code, value, timestamp] )
    except sqlite3 as e:
        print("Insert data error: %s" % e)
    con.commit()
    con.close()

def query_db(db_path, code):
    #print("Query DB ... ")
    con = sqlite3.connect( db_path )
    cur = con.cursor()
    sql_cmd = "SELECT value FROM code_table WHERE code = ? AND expired IS NULL"
    #print("sql_cmd = %s" % sql_cmd)
    try:
        cur.execute( sql_cmd, [code] )
    except sqlite3 as e:
        print("Query data error: %s" % e)
    ret = cur.fetchall()
    con.close()

    if len(ret) == 1:
        return ret[0][0]
    else:
        return ret

def check_expired(db_path):
    print("Checking expired code ... ")
    con = sqlite3.connect( db_path )
    cur = con.cursor()
    expired_time = time.monotonic_ns() - (1000000000 * 60 * 30)
    #print("Expired time => %s" % expired_time)
    sql_cmd = "SELECT CODE_ID, code, value FROM code_table WHERE timestamp < ?"
    #print("sql_cmd = %s" % sql_cmd)
    try:
        cur.execute( sql_cmd, [expired_time] )
    except sqlite3 as e:
        print("Query data error: %s" % e)
    ret = cur.fetchall()

    sql_cmd = "UPDATE code_table SET expired = 1 WHERE CODE_ID = ?"
    #print("sql_cmd = %s" % sql_cmd)
    for id, c, v in ret:
        #print("CODE_ID => %s, Code => %s, Value => %s" % (id, c, v))
        try:
            cur.execute( sql_cmd, [id] )
        except sqlite3 as e:
            print("Update for expired data error: %s" % e)
    con.commit()
    con.close()

def main():
    print("Starting code gen services ...")
    code, value, timestamp = code_gen()
    print("Code = %s, Value = %s, Timestamp = %s" % (code, value, timestamp))
    ret = code_verify(code)
    print("Code = %s, Ret Value = %s" % (code, ret))
    print("Execution time: %s s" % time.process_time())
    check_expired(code_db_path)
    print("Execution time: %s s" % time.process_time())


if __name__ == '__main__':
    main()