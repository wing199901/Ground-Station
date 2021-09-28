#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import math
import socket
from time import sleep

from fsuipc import FSUIPC
from paho.mqtt import client as mqtt


hostname = socket.gethostname()
# reset = False


def payload():
    # global reset
    with FSUIPC() as fsuipc:
        pause, pitot, ias, vertical_speed, compass, stall, overspeed, slip_skid, turn_rate, latitude, longitude,  pitch, roll, heading, heading_sel, altitude_sel, airspeed_sel, eng1_thro_lever, eng1_prop_lever, eng1_mix_lever, elevator_trim, parking_brake, landing_gear, flaps, pressure, mach, fuel_weight, angle_of_attack, side_slip, alternator, battery, avionics, fuel_pump, altitude, sim_stopped = prepared.read()

        payload = {
            'name': hostname,
            'time': datetime.datetime.now().strftime('%m/%d %H:%M:%S'),
            'pause': bool(pause),
            'reset': bool(pause) and bool(sim_stopped),
            'pitot': bool(pitot),
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
            'eng1': {
                'throttleLever': eng1_thro_lever / 16384 * 100,
                'propellerLever': eng1_prop_lever / 16384 * 100,
                'mixtureLever': eng1_mix_lever / 16384 * 100,
            },
            'elevatorTrim': elevator_trim / 16384 * 100,
            'parkingBrake': bool(parking_brake),
            'landingGear': bool(landing_gear),
            'flaps': flaps,
            'pressure': pressure / 16,
            'mach': mach / 20480,
            'fuelWeight': fuel_weight / 2.205,
            'aoa': math.degrees(angle_of_attack),
            'sideSlip': math.degrees(side_slip),
            'alternator': bool(alternator),
            'battery': bool(battery),
            'avionics': bool(avionics),
            'fuelPump': bool(fuel_pump),
            'altitude': altitude,
            'simStopped': bool(sim_stopped),
        }

        # print(payload)

    return payload


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(f"/Devices/{hostname}/Command", qos=2)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    message = json.loads(msg.payload)
    print(message)

    with FSUIPC() as fsuipc:
        if message['pause'] == True:
            fsuipc.write([(0x262, "H", 1)])
        elif message['pause'] == False:
            fsuipc.write([(0x262, "H", 0)])

        if message['reset'] == True:
            # "Situation reset" control (65591)
            fsuipc.write([(0x3110, "l", 65591)])

        # global reset
        # reset = message['reset']

        # while reset == True:
        #     if prepared.read()[0] == False:
        #         reset = False


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
    client.connect('192.168.0.128', 1883, 60)

    with FSUIPC() as fsuipc:
        prepared = fsuipc.prepare_data([
            (0x264, "H"),  # Pause Indicator
            (0x29C, "c"),  # Pitot
            (0x2BC, "d"),  # IAS
            (0x2C8, "d"),  # Vertical Speed
            (0x2CC, "d"),  # Compass
            (0x36C, "c"),  # Stall
            (0x36D, "c"),  # Overspeed
            (0x36E, "c"),  # Slip Skid
            # (0x372, "h"),  # Reliability
            (0x37C, "h"),  # Turn Rate
            # (0x55C, "d"),  # Init
            (0x560, "l"),  # Latitude
            (0x568, "l"),  # Longitude
            (0x578, "d"),  # Pitch
            (0x57C, "d"),  # Roll
            (0x580, "d"),  # Heading
            (0x7CC, "d"),  # Heading Sel
            (0x7D4, "d"),  # Altitude Sel
            (0x7E2, "d"),  # Airspeed Sel
            (0x88C, "h"),  # Engine 1 Throttle lever
            (0x88E, "h"),  # Engine 1 Propeller lever
            (0x890, "h"),  # Engine 1 Mixture lever
            (0xBC0, "h"),  # Elevator Trim
            (0xBC8, "h"),  # Parking Brake
            (0xBE8, "d"),  # Landing Gear
            (0xBFC, "c"),  # Flaps
            (0xEC6, "d"),  # Pressure
            (0x11C6, "d"),  # Mach
            (0x126C, "d"),  # Fuel Weight
            (0x2ED0, "f"),  # Angle of Attack
            (0x2ED8, "f"),  # Side Slip Angle
            (0x3101, "c"),  # Alternator
            (0x3102, "c"),  # Battery
            (0x3103, "c"),  # Avionics Master
            (0x3104, "c"),  # Fuel Pump
            (0x3324, "d"),  # Altitude
            (0x3365, "c"),  # In Menu or Dialog
            # (0x3BF8, "h"),  # Number of Flaps
        ], True)

    while True:
        client.publish(f"/Devices/{hostname}", json.dumps(payload()))
        client.loop()
