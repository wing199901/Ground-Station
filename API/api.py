from flask import Flask, jsonify, request
import mysql_operate as mysql

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/device', methods=['POST'])
# query device by session id
def get_all_devices_by_session_id():

    session = str(request.args.get('session_id'))

    sql = f"SELECT device.Name FROM device INNER JOIN session_device on device.id = session_device.device_id where session_device.session_id = {session};"
    data = mysql.db.select_db(sql)
    return jsonify(data)


@app.route('/add_device', methods=['POST'])
# add device to session
def add_device_to_session():
    device = str(request.args.get('device-id'))

    session = str(request.args.get('session_id'))

    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "No session"

    # check device exist
    sql = f"SELECT id FROM device WHERE id = '{device}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "No device"

    sql = f"INSERT INTO session_device VALUES('{session}','{device}');"
    mysql.db.execute_db(sql)
    return ""


# @app.route('/new_device', methods=['POST'])
# # register new device
# def new_device():
#     device = str(request.args.get('device_id'))

# # device id must be 3 letters or 4 letters
#     if not len(device) > 5 | len(device) < 3:
#         return "Not a propre device id."

#     name = "CONSOLE40-" + device if len(device) > 3 else "MODELA-" + device

#     sql = f"SELECT * FROM device WHERE id = '{device}';"
#     data = mysql.db.select_db(sql)

#     if data:
#         return "Already exists"
#     else:
#         sql = "INSERT INTO device values('" + device + "','" + name + "');"
#         mysql.db.execute_db(sql)
#         return ""


@app.route('/new_session', methods=['POST'])
# get new session id
def new_session():
    sql = "INSERT INTO session(StartTime) VALUES (CURRENT_TIMESTAMP)"

    # sql = """
    # START TRANSACTION;
    # INSERT INTO session(StartTime) VALUES (CURRENT_TIMESTAMP);
    # SELECT LAST_INSERT_ID();
    # COMMIT;
    # """

    mysql.db.execute_db(sql)
    # https://www.python.org/dev/peps/pep-0249/#lastrowid
    data = mysql.db.cursor.lastrowid
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
