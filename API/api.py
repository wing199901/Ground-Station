from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import mysql_operate as mysql
from mqtt_client import MyMQTTClass
from mqtt_config import *


app = Flask(__name__)
app.config["DEBUG"] = True
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

# mqtt client dict
mqtt_clients = {}


@app.route('/')
def index():
    return "Online"


# get all devices
@app.route('/api/devices', methods=['GET'])
def get_all_devices():
    # get data from database
    sql = f"SELECT id FROM device;"
    data = mysql.db.select_db(sql)

    return jsonify({'devices': data})


# get a device
@app.route('/api/devices/<string:device_id>', methods=['GET'])
def get_device(device_id):
    # device id must be 3 letters or 4 letters
    if len(device_id) != 3 and len(device_id) != 4:
        return make_response(jsonify({'error': f'{device_id} not a propre device id.'}), 404)

    # get data from database
    sql = f"SELECT * FROM device WHERE id = '{device_id}';"
    data = mysql.db.select_db(sql)

    if data:
        return jsonify({device_id: data})
    else:
        return make_response(jsonify({'error': f'Device id {device_id} does not exist.'}), 404)


# create new device
@app.route('/api/devices/<string:device_id>', methods=['POST'])
def create_device(device_id):
    # device id must be 3 letters or 4 letters
    if len(device_id) != 3 and len(device_id) != 4:
        return make_response(jsonify({'error': f'{device_id} not a propre device id.'}), 404)

    # full name of the device
    name = "CONSOLE40-" + \
        device_id if len(device_id) > 3 else "MODELA-" + device_id

    # check if the record already exists
    sql = f"SELECT * FROM device WHERE id = '{device_id}';"
    data = mysql.db.select_db(sql)

    if data:
        return make_response(jsonify({'error': f'Device id {device_id} already exists.'}), 404)
    else:
        sql = "INSERT INTO device values('" + device_id + "','" + name + "');"
        mysql.db.execute_db(sql)
        return "", 201


# get all session
@app.route('/api/sessions', methods=['GET'])
def get_all_session():
    sql = "SELECT id FROM session;"
    data = mysql.db.select_db(sql)
    return jsonify({"sessions": data})


# get session details
@app.route('/api/sessions/<int:session_id>', methods=['GET'])
def get_all_devices_by_session_id(session_id):
    sql = f"SELECT * FROM session WHERE id = {session_id};"
    mysql.db.cursor.execute(sql)
    data = mysql.db.cursor.fetchone()

    sql = f"SELECT device.id, device.name FROM device INNER JOIN session_device on device.id = session_device.device_id where session_device.session_id = {session_id};"
    device_data = mysql.db.select_db(sql)
    dict = {}
    data["devices"] = device_data
    dict["session"] = data

    if data:
        return jsonify(dict)
    else:
        return make_response(jsonify({'error': f'Session id {session_id} does not exist.'}), 404)


# create session
@app.route('/api/sessions', methods=['POST'])
def create_session():
    # sql = """
    # START TRANSACTION;
    # INSERT INTO session(StartTime) VALUES (CURRENT_TIMESTAMP);
    # SELECT LAST_INSERT_ID();
    # COMMIT;
    # """

    sql = "INSERT INTO session(startTime) VALUES (CURRENT_TIMESTAMP)"
    mysql.db.execute_db(sql)
    # https://www.python.org/dev/peps/pep-0249/#lastrowid
    data = mysql.db.cursor.lastrowid
    return jsonify({"session_id": data}), 201


# add device to session
@app.route('/api/sessions/<int:session_id>/<string:device_id>', methods=['POST'])
def add_device_to_session(session_id, device_id):
    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return make_response(jsonify({'error': f'Session id {session_id} does not exist.'}), 404)

    # device id must be 3 letters or 4 letters
    if len(device_id) != 3 and len(device_id) != 4:
        return make_response(jsonify({'error': f'{device_id} not a propre device id.'}), 404)

    # check device exist
    sql = f"SELECT id FROM device WHERE id = '{device_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return make_response(jsonify({'error': f'Device id {device_id} does not exist.'}), 404)

    sql = f"INSERT INTO session_device VALUES('{session_id}','{device_id}');"
    mysql.db.execute_db(sql)
    return "", 201


# query all flight data in session
@app.route('/api/flight_data/<int:session_id>', methods=['GET'])
def get_flight_data(session_id):
    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return make_response(jsonify({'error': f'Session id {session_id} does not exist.'}), 404)

    sql = f"SELECT * FROM data WHERE session_id = {session_id};"
    data = mysql.db.select_db(sql)
    data = {'flight_data': data}
    return jsonify(data)


# query flight data in session from a device
@app.route('/api/flight_data/<int:session_id>/<string:device_id>', methods=['GET'])
def get_device_flight_data(session_id, device_id):
    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return make_response(jsonify({'error': f'Session id {session_id} does not exist.'}), 404)

    # device id must be 3 letters or 4 letters
    if len(device_id) != 3 and len(device_id) != 4:
        return make_response(jsonify({'error': f'{device_id} not a propre device id.'}), 404)

    # check device exist
    sql = f"SELECT id FROM device WHERE id = '{device_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return make_response(jsonify({'error': f'Device id {device_id} does not exist.'}), 404)

    sql = f"SELECT * FROM data WHERE session_id = {session_id} AND device_id = '{device_id}';"
    data = mysql.db.select_db(sql)

    if data:
        return jsonify({device_id: data})
    else:
        return make_response(jsonify({'error': 'Flight data does not exist.'}), 404)


# trigger MQTT client to start recording flight data
@app.route('/api/start_session/<int:session_id>', methods=['POST'])
def start_recording(session_id):
    client = MyMQTTClass(session_id=session_id)
    client.run()

    # add client to clients dict
    mqtt_clients[session_id] = client
    return "", 200


# trigger MQTT client to stop record flight data
@app.route('/api/stop_session/<int:session_id>', methods=['POST'])
def stop_record(session_id):
    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return make_response(jsonify({'error': f'Session id {session_id} does not exist.'}), 404)

    try:
        client = mqtt_clients[session_id]
        client.stop()
        del mqtt_clients[session_id]
    except Exception as error:
        return make_response(jsonify({'error': f'{error}'}), 417)

    return "", 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': f'{error}'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
