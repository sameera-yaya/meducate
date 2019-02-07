from flask import render_template
from app import app
from six.moves import configparser
import MySQLdb
config = configparser.ConfigParser()

'''config.read('/../../mnt/c/Users/samee/Downloads/Meducate/flask/config.ini')
dbname = config.get('')'''

try:
    db_conn = MySQLdb.connect('localhost', 'syayavaram', 'G6nenw53', 'drug_info_db')
    cursor = db_conn.cursor()
except:
    print("Cannot connect to database")

print("Connected")

@app.route('/')
@app.route('/index')
def index():
    return render_template("meds.html")
