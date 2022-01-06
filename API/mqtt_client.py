import paho.mqtt.client as mqtt
from mqtt_config import *
import json
import mysql_operate as mysql


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC, qos=0)


def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    # is topic from devices
    if "Device" in msg.topic:
        message = json.loads(msg.payload)

        # start insert data to db
        payload_to_db(message)


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)


client = mqtt.Client()

# Assign event callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect to the Broker
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

# client.loop_forever()

# init session id
session_id = 0


# mqtt payload insert into database
def payload_to_db(dict):
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

    device_id = name.split("-")[1]

    sql = f"INSERT INTO data VALUES(NULL, {session_id}, '{device_id}', '{time}', {navigation}, {beacon}, {landing}, {taxi}, {strobes}, {pitot}, {ias}, {verticalSpeed}, {whiskeyCompass}, {stall}, {overspeed}, {slipSkid}, {turnRate}, {pitch}, {roll}, {heading}, {autopilot}, {headingSel}, {altitudeSel}, {airspeedSel}, {throttleLever}, {propellerLever}, {mixtureLever}, {magnetos}, {rpm}, {maxRPM}, {fuelSelector}, {elevatorTrim}, {parkingBrake}, {landingGear}, {flaps}, {pressure}, {mach}, {fuelWeight}, {aoa}, {sideSlip}, {flightDirector}, {flightDirectorPitch}, {flightDirectorBank}, {alternator}, {battery}, {avionics}, {fuelPump}, {altitude}, {elevatorAxis}, {aileronAxis}, {latitude}, {longitude}, '{status}')"
    print(sql)
    mysql.db.execute_db(sql)
