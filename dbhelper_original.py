import pymysql
import config
import os

config = config.Dev_Cloud()


host = config.host
db_user = config.db_user
db_password = config.db_password
port = config.port



#---------------GOOGLE CLOUD MYSQL -----------
# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`

class DBHelper:
    ''' CRUD
        Create, Read, Update, Delete
        '''

    def connect(self, db_name="crimemap"):
        if os.environ.get('GAE_ENV') == 'standard':
                db_user = os.environ.get('CLOUD_SQL_USERNAME')
                db_password = os.environ.get('CLOUD_SQL_PASSWORD')
                db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
                db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
                # If deployed, use the local socket interface for accessing Cloud SQL
                unix_socket = '/cloudsql/{}'.format(db_connection_name)
                cnx = pymysql.connect(user=db_user, password=db_password,
                                        unix_socket=unix_socket, db=db_name)
        else:
                # If running locally, use the TCP connections instead
                # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
                # so that your application can use 127.0.0.1:3306 to connect to your
                # Cloud SQL instance
                cnx = pymysql.connect(user=db_user, port=port, password=db_password,
                                        host=host, db=db_name)
                return cnx

        with cnx.cursor() as cursor:
                cursor.execute('SELECT NOW() as now;')
                result = cursor.fetchall()
                current_time = result[0][0]
                print('Connection made at: ',str(current_time))
    #---------------END GOOGLE CLOUD MYSQL -----------



    # def connect(self, database="crimemap"):
    #     return pymysql.connect(host='localhost',
    #             user=config.db_user,
    #             passwd=config.db_password,
    #             db=database)


    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                query ="INSERT INTO crimes (category, date, latitude, longitude, description) VALUES (%s, %s, %s, %s, %s);"
                
                print(query)
                cursor.execute(query, (category, date, latitude, longitude, description))
                print('before commit')
                connection.commit()
                print('after commit')
        except Exception as e:
            print('this is your stupid e:',e)
        finally:
            connection.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            #introduces deliberate security flaw - SQL injection
            query = "INSERT INTO crimes (description) VALUES (%s);" # the variable in %s will be places cursor.execute
            with connection.cursor() as cursor:
                cursor.execute(query, data) # variable data will be placed into query and will be checked for SQL injection
                connection.commit()
        finally:
            connection.close()

    def get_all_crimes(self):
        connection = self.connect()
        try:
            query = 'SELECT * FROM crimes'
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
                print('fetched the data')
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()

