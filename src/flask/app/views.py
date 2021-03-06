from flask import render_template
from app import app
import pandas as pd
from six.moves import configparser
import MySQLdb
from flask import request
import plotly
import json

config = configparser.ConfigParser()

config.read('/home/ubuntu/meducate/src/flask/app/config.ini')
dbname = config.get('auth', 'dbname')
dbuser = config.get('auth', 'user')
dbpass = config.get('auth', 'password')
dbhost = config.get('auth', 'host')
dbport = config.get('auth', 'port')
'''
try:
    db_conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=dbname)
    cursor = db_conn.cursor()
except:
    print("Cannot connect to database")

print("Connected")
'''
@app.route('/')
@app.route('/index')
def index():
    return render_template("meds.html")

@app.route('/graph')
def graph():
    try:
        db_conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=dbname)
        cursor = db_conn.cursor()
    except:
        print("Cannot connect to database")

    print("Connected")
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
    db_conn.close()

    results = []
    for i in range (0, sql_query_results.shape[0]):
	results.append(dict(name=sql_query_results.iloc[i]['name'],
			rating=sql_query_results.iloc[i]['rating']))

    graph_results = sql_query_results.head()

    names = map(str, list(graph_results['name'].values))
    #names = map(str, list(sql_query_results['name'].values))
    ratings = map(float, list(graph_results['rating'].values))
    print(names)
    print(ratings)
    graph = [
	dict(
	    data=[
		dict(
		    x=names,
		    y=ratings,
		    type='bar'
		)],
	)
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graph)]
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)



    return render_template("charts.html", results = results,ids=ids, graph_results = graphJSON)






