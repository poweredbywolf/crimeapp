import pymysql
import config

config = config.Config()

class DBHelper:
    ''' CRUD
        Create, Read, Update, Delete
        '''

    def connect(self, database="crimemap"):
        return pymysql.connect(host='localhost',
                user=config.db_user,
                passwd=config.db_password,
                db=database)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = 'SELECT description FROM crimes;'
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

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

