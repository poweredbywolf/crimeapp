from flask import Flask
from os import environ

app = Flask(__name__)


# The states the app can be are the following
# Deployed and Production and Connected to Cloud SQL
# Local Environ and Development Environment
#
# Local and connected to Local DB
# Local and Connected to production DB - Cloud SQL through a local client

if environ.get('DEPLOYED_STATE') == 'APP_Engine_Cloud_Sql':
    DB_CONNECTION_NAME = environ.get('CLOUD_SQL_CONNECTION_NAME') #when deployed it uses the uniqe connection name and not an IP address
    DB_HOST = DB_CONNECTION_NAME
    DB_USER = environ.get('CLOUD_SQL_USERNAME')
    DB_PW = environ.get('CLOUD_SQL_PASSWORD')
    DATABASE = environ.get('CLOUD_SQL_DATABASE_NAME')
    PORT = environ.get('PORT')
    MAPS_API_K = environ.get('MAPS_API_K')

  
elif environ.get('DEPLOYED_STATE') == 'Dev_CloudSql': #remember to: export DEPLOYED_STATE=Dev_CloudSql
    print('Mode:Dev_CloudSql')
    app.config.from_object('config.Dev_CloudSql')
    DB_HOST = app.config.get('DB_HOST')
    DB_PW = app.config.get('DB_PW')
    DATABASE = app.config.get('DATABASE')
    PORT = app.config.get('PORT')
    MAPS_API_K = app.config.get('MAPS_API_K')
    print(MAPS_API_K)
else:
    app.config.from_object('config.Development')
    DB_HOST = app.config.get('DB_HOST')
    DB_PW = app.config.get('DB_PW')
    DATABASE = app.config.get('DATABASE')
    PORT = app.config.get('PORT')
    MAPS_API_K = app.config.get('MAPS_API_K')


from applications import routes