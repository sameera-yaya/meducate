from flask import render_template
from app import app
from six.moves import configparser
import MySQLdb
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
    sql_query = '''
                SELECT * FROM druginfo;
                '''
    return render_template("charts.html")
