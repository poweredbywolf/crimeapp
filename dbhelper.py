import pymysql
from os import environ

# import configuration

# conf = configuration.Configuration()

# DB_CONNECTION_NAME = conf.DB_CONNECTION_NAME
# DB_HOST  = conf.DB_HOST
# DB_USER  = conf.DB_USER
# DB_PW = conf.DB_PW
# DATABASE = conf.DATABASE
# PORT = conf.PORT

DB_CONNECTION_NAME = environ.get('DB_CONNECTION_NAME') #when deployed it uses the uniqe connection name and not an IP address
DB_HOST = environ.get('DB_HOST')
DB_USER = environ.get('DB_USER')
DB_PW = environ.get('DB_PW')
DATABASE = environ.get('DATABASE')
DB_PORT = int(environ.get('DB_PORT'))


#---------------GOOGLE CLOUD MYSQL -----------
# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`

class DBHelper:
    ''' CRUD
        Create, Read, Update, Delete
        '''

    def connect(self, db_name="crimemap"):
        if environ.get('GAE_ENV') == 'standard':
                # If deployed, use the local socket interface for accessing Cloud SQL
                unix_socket = '/cloudsql/{}'.format(DB_CONNECTION_NAME)
                cnx = pymysql.connect(user=DB_USER, password=DB_PW,
                                        unix_socket=unix_socket, db=DATABASE)
        else:
                # If running locally, use the TCP connections instead
                # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
                # so that your application can use 127.0.0.1:3306 to connect to your
                # Cloud SQL instance
                cnx = pymysql.connect(user=DB_USER, port=DB_PORT, password=DB_PW,
                                        host=DB_HOST, db=DATABASE)
        return cnx

        with cnx.cursor() as cursor:
                cursor.execute('SELECT NOW() as now;')
                result = cursor.fetchall()
                current_time = result[0][0]
                print('Connection made at: ',str(current_time))
    #---------------END GOOGLE CLOUD MYSQL -----------




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