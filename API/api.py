from flask import Flask, jsonify, request
import mysql_operate as mysql
from mqtt_client import MyMQTTClass
from mqtt_config import *


app = Flask(__name__)
app.config["DEBUG"] = True

# mqtt client dict
clients = {}


# register new device
@app.route('/register_device', methods=['POST'])
def new_device():
    device = str(request.args.get('device_id'))
    print(device)
    print(len(device))

# device id must be 3 letters or 4 letters
    if len(device) != 3 and len(device) != 4:
        return "Not a propre device id."

    name = "CONSOLE40-" + device if len(device) > 3 else "MODELA-" + device

    sql = f"SELECT * FROM device WHERE id = '{device}';"
    data = mysql.db.select_db(sql)

    if data:
        return "Already exists"
    else:
        sql = "INSERT INTO device values('" + device + "','" + name + "');"
        mysql.db.execute_db(sql)
        return ""


# get new session id
@app.route('/new_session', methods=['POST'])
def new_session():
    sql = "INSERT INTO session(startTime) VALUES (CURRENT_TIMESTAMP)"

    # sql = """
    # START TRANSACTION;
    # INSERT INTO session(StartTime) VALUES (CURRENT_TIMESTAMP);
    # SELECT LAST_INSERT_ID();
    # COMMIT;
    # """

    mysql.db.execute_db(sql)
    # https://www.python.org/dev/peps/pep-0249/#lastrowid
    data = mysql.db.cursor.lastrowid
    data = {"session_id": data}
    return jsonify(data)


# add device to session
@app.route('/add_device', methods=['POST'])
def add_device_to_session():
    device = str(request.args.get('device_id'))

    session = str(request.args.get('session_id'))

    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "Wrong session id"

    # check device exist
    sql = f"SELECT id FROM device WHERE id = '{device}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "Wrong device id"

    sql = f"INSERT INTO session_device VALUES('{session}','{device}');"
    mysql.db.execute_db(sql)
    return ""


# query device by session id
@app.route('/query', methods=['POST'])
def get_all_devices_by_session_id():

    session = str(request.args.get('session_id'))

    sql = f"SELECT device.id, device.name FROM device INNER JOIN session_device on device.id = session_device.device_id where session_device.session_id = {session};"
    data = mysql.db.select_db(sql)
    data = {"devices": data}
    return jsonify(data)


# trigger MQTT client to start recording flight data
@app.route('/start_session', methods=['POST'])
def start_record():
    session = str(request.args.get('session_id'))

    client = MyMQTTClass(session_id=session)
    client.run()

    # add client to clients dict
    clients[session] = client
    return ""


# trigger MQTT client to stop record flight data
@app.route('/stop_session', methods=['POST'])
def stop_record():
    session = str(request.args.get('session_id'))

    try:
        client = clients[session]
        client.stop()
        del clients[session]
    except:
        return "Session not exists"
    return ""


# query flight data by session id
@app.route('/query_flight_data', methods=['POST'])
def get_all_flight_data_by_session_id():
    device = str(request.args.get('device_id'))

    session = str(request.args.get('session_id'))

    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "Wrong session id"

    # check device exist
    sql = f"SELECT id FROM device WHERE id = '{device}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "Wrong device id"

    sql = f"SELECT * FROM data WHERE session_id = {session} AND device_id = '{device}';"
    data = mysql.db.select_db(sql)
    data = {device: data}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
