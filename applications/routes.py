



from dbhelper import DBHelper
from flask import render_template, request
import datetime
import dateparser
import json
import string


import config
from applications import app


DB = DBHelper()
categories = ['mugging', 'break-in']
crimes = ['assault', 'other']
maps_api_key = config.maps_api_key
#-------------------------
# Functions
#-------------------------
def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None    

def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    sanitized_list = list(filter(lambda x: x in whitelist, userinput))
    listToStr = ' '.join(map(str, sanitized_list)) 
    return listToStr
# -------------------------
# Routes
#-------------------------

@app.route('/')
def home(error_msg=None):
    print('I am at home function')
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(e)
    return render_template("home.html", crimes=crimes, categories=categories, error_msg=error_msg, maps_api_key=maps_api_key)


@app.route('/add', methods=['POST'])
def add():
    try:
        data = request.form.get('userinput')
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()

@app.route('/clear', methods=['POST'])
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


@app.route('/submitcrime', methods=['POST'])
def submitcrime():
    print('Request Object: \n', 'Full Path:',request.full_path, '\n Headers:', request.headers,'\n Request Dict:',request.__dict__, '\n ---------- End of Request object to Submit Crime ----------- ')
    category = request.form.get('category') 
    if category not in categories:
        return home()   
    date = format_date(request.form.get('date'))    
    if not date:
        return home('Invalid date. Please use YYYY/MM/DD format')
    try:
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
    except ValueError:
        return home()
    description = sanitize_string(request.form.get('description'))
    print('Type',type(description))
    print(description)
    DB.add_crime(category, date, latitude, longitude, description)
    return mapjs()


# --------------------------------------------------------------------
@app.route('/mapjs')
def mapjs():
    return render_template('mapJS.html', crimes=crimes, categories=categories, maps_api_key=maps_api_key)

@app.route('/mapclick')
def mapClick():
    return render_template('mapclick.html', maps_api_key=maps_api_key)


@app.route('/geo')
def geo():
    return render_template('mapsGeo.html', maps_api_key=maps_api_key)



# --------------------------------------------------------------------