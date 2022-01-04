from flask import Flask, jsonify, request
import mysql_operate as mysql

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def index():
    return "hello world"

@app.route('/devices')
def getAllDevices():
    sql = "SELECT * FROM device"
    data = mysql.db.select_db(sql)
    return jsonify(data)


@app.route('/newSession')
def newSession():
    sql = "" 
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
