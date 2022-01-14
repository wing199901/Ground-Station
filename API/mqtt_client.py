import paho.mqtt.client as mqtt
from mqtt_config import *
import mysql_operate as mysql
import random
import json


class MyMQTTClass:
    # init session id
    session_id = 0

    def __init__(self, session_id=0):
        self._client = mqtt.Client(client_id=f"API-{random.randint(0, 1000)}")
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.on_subscribe = self.on_subscribe
        self.session_id = session_id

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

        # check device topic
        if "Device" in msg.topic:
            message = json.loads(msg.payload)

            # start insert data to db
            payload_to_db(message, self.session_id)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("On Subscribed: qos = %d" % granted_qos)

    def run(self):
        self._client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        self._client.subscribe(MQTT_TOPIC, qos=1)
        self._client.loop_start()

    def stop(self):
        self._client.loop_stop()


# mqtt payload insert into database
def payload_to_db(dict, session_id):
    name = dict['name']
    time = dict['time']
    navigation = dict['lights']['navigation']
    beacon = dict['lights']['beacon']
    landing = dict['lights']['landing']
    taxi = dict['lights']['taxi']
    strobes = dict['lights']['strobes']
    pitot = dict['pitot']
    ias = dict['ias']
    verticalSpeed = dict['verticalSpeed']
    whiskeyCompass = dict['whiskeyCompass']
    stall = dict['stall']
    overspeed = dict['overspeed']
    slipSkid = dict['slipSkid']
    turnRate = dict['turnRate']
    pitch = dict['pitch']
    roll = dict['roll']
    heading = dict['heading']
    autopilot = dict['autopilot']
    headingSel = dict['headingSel']
    altitudeSel = dict['altitudeSel']
    airspeedSel = dict['airspeedSel']
    throttleLever = dict['eng1']['throttleLever']
    propellerLever = dict['eng1']['propellerLever']
    mixtureLever = dict['eng1']['mixtureLever']
    magnetos = dict['eng1']['magnetos']
    rpm = dict['eng1']['rpm']
    maxRPM = dict['eng1']['maxRPM']
    fuelSelector = dict['fuelSelector']
    elevatorTrim = dict['elevatorTrim']
    parkingBrake = dict['parkingBrake']
    landingGear = dict['landingGear']
    flaps = dict['flaps']
    pressure = dict['pressure']
    mach = dict['mach']
    fuelWeight = dict['fuelWeight']
    aoa = dict['aoa']
    sideSlip = dict['sideSlip']
    flightDirector = dict['flightDirector']
    flightDirectorPitch = dict['flightDirectorPitch']
    flightDirectorBank = dict['flightDirectorBank']
    alternator = dict['alternator']
    battery = dict['battery']
    avionics = dict['avionics']
    fuelPump = dict['fuelPump']
    altitude = dict['altitude']
    elevatorAxis = dict['elevatorAxis']
    aileronAxis = dict['aileronAxis']
    latitude = dict['latitude']
    longitude = dict['longitude']
    status = dict['status']

    # e.g. CONSOLE40-XXXX
    device_id = name.split("-")[1]

    # check session exist
    sql = f"SELECT id FROM session WHERE id = '{session_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "Wrong session id"

    # check device exist
    sql = f"SELECT id FROM device WHERE id = '{device_id}';"
    data = mysql.db.select_db(sql)

    if not data:
        return "Wrong device id"

    sql = f"INSERT INTO data VALUES(NULL, {session_id}, '{device_id}', '{time}', {navigation}, {beacon}, {landing}, {taxi}, {strobes}, {pitot}, {ias}, {verticalSpeed}, {whiskeyCompass}, {stall}, {overspeed}, {slipSkid}, {turnRate}, {pitch}, {roll}, {heading}, {autopilot}, {headingSel}, {altitudeSel}, {airspeedSel}, {throttleLever}, {propellerLever}, {mixtureLever}, {magnetos}, {rpm}, {maxRPM}, {fuelSelector}, {elevatorTrim}, {parkingBrake}, {landingGear}, {flaps}, {pressure}, {mach}, {fuelWeight}, {aoa}, {sideSlip}, {flightDirector}, {flightDirectorPitch}, {flightDirectorBank}, {alternator}, {battery}, {avionics}, {fuelPump}, {altitude}, {elevatorAxis}, {aileronAxis}, {latitude}, {longitude}, '{status}')"
    print(sql)
    mysql.db.execute_db(sql)
    return ""
