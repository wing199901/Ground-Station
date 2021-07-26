#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import math
import socket

from fsuipc import FSUIPC
from paho.mqtt import client as mqtt


def payload():
    with FSUIPC() as fsuipc:

        pause, ias, vertical_speed, compass, stall, overspeed, slip_skid, turn_rate, latitude, longitude,  pitch, roll, heading, heading_sel, altitude_sel, airspeed_sel, pressure, mach, angle_of_attack, side_slip,  altitude = prepared.read()

        print(f"Pause: {pause}")
        print(f"IAS: {ias}")
        print(f"Vertical Speed: {vertical_speed}")
        print(f"Compass: {compass}")
        print(f"Stall: {stall}")
        print(f"Overspeed: {overspeed}")
        print(f"Slip Skid: {slip_skid}")
        print(f"Turn Rate: {turn_rate}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Pitch: {pitch}")
        print(f"Roll: {roll}")
        print(f"Heading: {heading}")
        print(f"HeadingSel: {heading_sel}")
        print(f"AltitudeSel: {altitude_sel}")
        print(f"AirspeedSel: {airspeed_sel}")
        print(f"Pressure: {pressure}")
        print(f"Mach: {mach}")
        print(f"Angle of Attack: {angle_of_attack}")
        print(f"Side Slip: {side_slip}")
        print(f"Altitude: {altitude}")

        payload = {
            'name': socket.gethostname(),
            'time': datetime.datetime.now().strftime('%m/%d %H:%M:%S'),
            'pause': bool(pause),
            'ias': ias / 128,
            'verticalSpeed': vertical_speed * 60 * 3.28084 / 256,
            'compass': compass,
            'stall': bool(stall),
            'overspeed': bool(overspeed),
            'slipSkid': slip_skid,
            'turnRate': turn_rate,
            'latitude': latitude * 90.0/(10001750.0 * 65536.0 * 65536.0),
            'longitude': longitude * 360.0/(65536.0 * 65536.0 * 65536.0 * 65536.0),
            'pitch': pitch * 360 / (65536*65536)*(-1),
            'roll': roll * 360 / (65536*65536)*(-1),
            'heading': heading * 360 / (65536*65536),
            'headingSel': heading_sel / 65536 * 360,
            'altitudeSel': altitude_sel / 65536 * 3.281,
            'airspeedSel': airspeed_sel,
            'pressure': pressure / 16,
            'mach': mach / 20480,
            'aoa': math.degrees(angle_of_attack),
            'sideSlip': math.degrees(side_slip),
            'altitude': altitude,
        }

    return payload


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/Sensors/ModelA/Command", qos=2)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    message = json.loads(msg.payload)

    print(message)

    with FSUIPC() as fsuipc:
        if message['pause'] == True:
            fsuipc.write([(0x262, "H", 1)])
        else:
            fsuipc.write([(0x262, "H", 0)])


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)


def on_disconnect(client, userdata, rc=0):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


if __name__ == "__main__":
    # client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)
    client = mqtt.Client()
    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect

    # Connect to the Broker
    # client.connect('aerosimmqtt.eastasia.azurecontainer.io', 1883, 60)
    client.connect('192.168.0.129', 1883, 60)

    client.loop_start()

    with FSUIPC() as fsuipc:
        prepared = fsuipc.prepare_data([
            (0x264, "H"),  # Pause Indicator
            (0x2BC, "d"),  # IAS
            (0x2C8, "d"),  # Vertical Speed
            (0x2CC, "d"),  # Compass
            (0x36C, "c"),  # Stall
            (0x36D, "c"),  # Overspeed
            (0x36E, "c"),  # Slip Skid
            (0x37C, "h"),  # Turn Rate
            (0x560, "l"),  # Latitude
            (0x568, "l"),  # Longitude
            (0x578, "d"),  # Pitch
            (0x57C, "d"),  # Roll
            (0x580, "d"),  # Heading
            (0x7CC, "d"),  # Heading Sel
            (0x7D4, "d"),  # Altitude Sel
            (0x7E2, "d"),  # Airspeed Sel
            (0xEC6, "d"),  # Pressure
            (0x11C6, "d"),  # Mach
            (0x2ED0, "f"),  # Angle of Attack
            (0x2ED8, "f"),  # Side Slip Angle
            (0x3324, "d"),  # Altitude
        ], True)

    while client.loop() == 0:
        client.publish("/Sensors/ModelA", json.dumps(payload()))
