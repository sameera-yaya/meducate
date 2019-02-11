from flask import render_template
from app import app
import pandas as pd
from six.moves import configparser
import MySQLdb
from flask import request

config = configparser.ConfigParser()

config.read('/home/ubuntu/insight-drug-info/flask/app/config.ini')
dbname = config.get('auth', 'dbname')
dbuser = config.get('auth', 'user')
dbpass = config.get('auth', 'password')
dbhost = config.get('auth', 'host')
dbport = config.get('auth', 'port')

try:
    db_conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=dbname)
    cursor = db_conn.cursor()
except:
    print("Cannot connect to database")

print("Connected")

@app.route('/')
@app.route('/index')
def index():
    return render_template("meds.html")

@app.route('/graph')
def graph():
    loc = request.args.get('diagnosis')
    sql_query = "SELECT name, avg(rating) as rating\
		FROM druginfo\
		WHERE diagnosis = '%s'\
		GROUP BY name\
		ORDER BY rating desc"\
		%(loc)
    print(sql_query)
    sql_query_results = pd.read_sql_query(sql_query, db_conn)
    print(sql_query_results)
    results = []
    for i in range (0, sql_query_results.shape[0]):
	results.append(dict(name=sql_query_results.iloc[i]['name'],\
			rating=sql_query_results.iloc[i]['rating']))

    return render_template("charts.html", results = results)
