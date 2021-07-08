#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import math
import socket

import paho.mqtt.client as mqtt
from fsuipc import FSUIPC


# Define event callbacks
def on_connect(mqttc, obj, flags, rc):
    print("connect rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_log(mqttc, obj, level, string):
    print(string)


if __name__ == "__main__":
    client = mqtt.Client()
    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    # Uncomment to enable debug messages
    client.on_log = on_log

    # Connect to the Broker
    # client.connect('aerosimmqtt.eastasia.azurecontainer.io', 1883, 60)
    client.connect('192.168.0.225', 1883, 60)

    client.loop_start()

    with FSUIPC() as fsuipc:
        prepared = fsuipc.prepare_data([
            (0x2BC, "d"),  # IAS
            (0x2C8, "d"),  # Vertical Speed
            (0x2CC, "d"),  # Compass
            (0x36C, "c"),  # Stall
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

        while True:
            ias, vertical_speed, compass, stall, slip_skid, turn_rate, latitude, longitude,  pitch, roll, heading, heading_sel, altitude_sel, airspeed_sel, pressure, mach, angle_of_attack, side_slip,  altitude = prepared.read()

            print(f"IAS: {ias}")
            print(f"Vertical Speed: {vertical_speed}")
            print(f"Compass: {compass}")
            print(f"Stall: {stall}")
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
                'Name': socket.gethostname(),
                'Time': datetime.datetime.now().strftime('%m/%d %H:%M:%S'),
                'IAS': ias / 128,
                'Vertical Speed': vertical_speed * 60 * 3.28084 / 256,
                'Compass': compass,
                'Stall': bool(stall),
                'Slip Skid': slip_skid,
                'Turn Rate': turn_rate,
                'Latitude': latitude * 90.0/(10001750.0 * 65536.0 * 65536.0),
                'Longitude': longitude * 360.0/(65536.0 * 65536.0 * 65536.0 * 65536.0),
                'Pitch': pitch * 360 / (65536*65536)*(-1),
                'Roll': roll * 360 / (65536*65536)*(-1),
                'Heading': heading * 360 / (65536*65536),
                'HeadingSel': heading_sel / 65536 * 360,
                'AltitudeSel': altitude_sel / 65536 * 3.281,
                'AirspeedSel': airspeed_sel,
                'Pressure': pressure / 16,
                'Mach': mach / 20480,
                'AOA': math.degrees(angle_of_attack),
                'Side Slip': math.degrees(side_slip),
                'Altitude': altitude,
            }

            client.publish("/Sensor/ModelA", json.dumps(payload))
