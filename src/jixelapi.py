from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

#CORS
CORS(app)

#My SQL
mysql = MySQL()

#Configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'jixel'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
conn = mysql.connect()
cur = conn.cursor()

@app.route("/")
def hello():
    return "API"

#GET Unknown Info
@app.route("/unknown")
def get():
    cur.execute('''select * from jixel.unknowntable''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(r);

#GET Reported Info
@app.route("/reported")
def get1():
    cur.execute('''select * from jixel.missingtable''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myCollection' : r});

#POST UnknownInfo
@app.route("/postuk", methods=['POST'])
def postuk():
    _id = '4'
    _picture = '4'
    _timestamp = '4'
    cur.execute('''SELECT MAX(id) FROM `jixel`.`unknowntable`''')
    maxid = cur.fetchone()
    cur.execute('''INSERT INTO `jixel`.`unknowntable` (`id`, `timestamp`, `picturename`) VALUES (%s,NULL,%s);''', (maxid[0]+1, maxid[0]+1))
    conn.commit()
    return "Done"

#POST ReportedInfo
@app.route("/postrptd/<reportername>/<reporteremail>/<missingname>/<picturename>", methods=['POST'])
def postrptd(reportername, reporteremail, missingname, picturename):
    cur.execute('''SELECT MAX(id) FROM `jixel`.`missingtable`''')
    maxid = cur.fetchone()
    cur.execute('''INSERT INTO `jixel`.`missingtable` (`id`,`timestamp`,`reportername`,`reporteremail`, `missingname`, `picturename`) VALUES (%s, NULL, %s, %s, %s, %s);''', (maxid[0]+1, reportername, reporteremail, missingname, picturename))
    conn.commit()
    return "Done"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)