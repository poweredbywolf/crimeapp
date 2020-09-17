import pymysql
# import dbconfig
import os
from flask import jsonify

# connection = pymysql.connect(host='localhost',
#                              user=dbconfig.db_user,
#                              passwd=dbconfig.db_password)





# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`
if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        db_user = 'z_sql'
        db_password = 'Guitar1!'
        port = 3307
        cnx = pymysql.connect(user=db_user, port=port, password=db_password,
                                host=host)

with cnx.cursor() as cursor:
        cursor.execute('SELECT NOW() as now;')
        result = cursor.fetchall()
        current_time = result[0][0]
        print(str(current_time))
        
        


try:
        with cnx.cursor() as cursor:
                sql = "CREATE DATABASE IF NOT EXISTS crimemap"
                cursor.execute(sql)
                sql = """CREATE TABLE IF NOT EXISTS crimemap.crimes (
id int NOT NULL AUTO_INCREMENT,
latitude FLOAT(10,6),
longitude FLOAT(10,6),
date DATETIME,
category VARCHAR(50),
description VARCHAR(1000),
updated_at TIMESTAMP,
PRIMARY KEY (id)
)"""
                cursor.execute(sql)
        cnx.commit()
finally:
        cnx.close()