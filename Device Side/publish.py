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


def payload():

    with FSUIPC() as fsuipc:
        lights, pause, pitot, ias, vertical_speed, whiskey_compass, stall, overspeed, slip_skid, turn_rate, pitch, roll, heading, autopilot, heading_sel, altitude_sel, airspeed_sel, eng1_thro_lever, eng1_prop_lever, eng1_mix_lever, eng1_magnetos, fuel_selector, elevator_trim, parking_brake, landing_gear, flaps, pressure, mach, fuel_weight, eng1_rpm, eng1_max_rpm, angle_of_attack, side_slip, flight_director, flight_director_pitch, flight_director_bank, alternator, battery, avionics, fuel_pump,  altitude, elevator_axis, aileron_axis, sim_in_menu, latitude, longitude = prepared.read()

        payload = {
            'name': hostname,
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'lights': {
                'navigation': bool((lights >> 0) & 1),
                'beacon': bool((lights >> 1) & 1),
                'landing': bool((lights >> 2) & 1),
                'taxi': bool((lights >> 3) & 1),
                'strobes': bool((lights >> 4) & 1),
                # 'instruments': bool((lights >> 5) & 1),
                # 'recognition': bool((lights >> 6) & 1),
                # 'wing': bool((lights >> 7) & 1),
                # 'logo': bool((lights >> 8) & 1),
                # 'cabin': bool((lights >> 9) & 1),
            },
            'pitot': bool(pitot),
            'ias': ias / 128,
            'verticalSpeed': vertical_speed * 60 * 3.28084 / 256,
            'whiskeyCompass': whiskey_compass,
            'stall': bool(stall),
            'overspeed': bool(overspeed),
            'slipSkid': slip_skid,
            'turnRate': turn_rate,
            'pitch': pitch * 360 / (65536*65536)*(-1),
            'roll': roll * 360 / (65536*65536)*(-1),
            'heading': heading * 360 / (65536*65536),
            'autopilot': bool(autopilot),
            'headingSel': heading_sel / 65536 * 360,
            'altitudeSel': altitude_sel / 65536 * 3.281,
            'airspeedSel': airspeed_sel,
            'eng1': {
                'throttleLever': eng1_thro_lever / 16384 * 100,
                'propellerLever': eng1_prop_lever / 16384 * 100,
                'mixtureLever': eng1_mix_lever / 16384 * 100,
                'magnetos': eng1_magnetos,
                'rpm': eng1_rpm,
                'maxRPM': eng1_max_rpm,
            },
            'fuelSelector': fuel_selector,
            'elevatorTrim': elevator_trim / 16384 * 100,
            'parkingBrake': bool(parking_brake),
            'landingGear': bool(landing_gear),
            'flaps': flaps,
            'pressure': pressure / 16,
            'mach': mach / 20480,
            'fuelWeight': fuel_weight / 2.205,
            'aoa': math.degrees(angle_of_attack),
            'sideSlip': math.degrees(side_slip),
            'flightDirector': bool(flight_director),
            'flightDirectorPitch': flight_director_pitch,
            'flightDirectorBank': flight_director_bank,
            'alternator': bool(alternator),
            'battery': bool(battery),
            'avionics': bool(avionics),
            'fuelPump': bool(fuel_pump),
            'altitude': altitude,
            'elevatorAxis': elevator_axis,
            'aileronAxis': aileron_axis,
            'latitude': latitude,
            'longitude': longitude,
            'status': getStatus(pause, sim_in_menu),
        }

    return payload


def getStatus(pause, sim_in_menu):
    if bool(pause) and bool(sim_in_menu):
        return "resetting"
    elif bool(pause):
        return "pausing"
    elif bool(sim_in_menu):
        return "in_menu"
    else:
        return "normal"


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

    # setup last will
    client.will_set(
        f"/Devices/{hostname}",
        json.dumps({'status': "offline", }),
        qos=0,
        retain=False
    )

    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect

    # Connect to the Broker
    # client.connect('aerosimmqtt.eastasia.azurecontainer.io', 1883, 60)
    client.connect('192.168.0.233', 1883, 60)

    with FSUIPC() as fsuipc:
        prepared = fsuipc.prepare_data([
            (0xD0C, "h"),  # Lights
            (0x264, "h"),  # Pause Indicator
            (0x29C, "c"),  # Pitot
            (0x2BC, "d"),  # IAS
            (0x2C8, "d"),  # Vertical Speed
            (0x2CC, "f"),  # Whiskey Compass
            (0x36C, "c"),  # Stall
            (0x36D, "c"),  # Overspeed
            (0x36E, "c"),  # Slip Skid
            (0x37C, "h"),  # Turn Rate
            (0x578, "d"),  # Pitch
            (0x57C, "d"),  # Roll
            (0x580, "d"),  # Heading
            (0x7BC, "d"),  # Autopilot
            (0x7CC, "d"),  # Heading Sel
            (0x7D4, "d"),  # Altitude Sel
            (0x7E2, "d"),  # Airspeed Sel
            (0x88C, "h"),  # Engine 1 Throttle lever
            (0x88E, "h"),  # Engine 1 Propeller lever
            (0x890, "h"),  # Engine 1 Mixture lever
            (0x892, "h"),  # Engine 1 Magnetos
            (0xAF8, "h"),  # Fuel Selector
            (0xBC0, "h"),  # Elevator Trim
            (0xBC8, "h"),  # Parking Brake
            (0xBE8, "d"),  # Landing Gear
            (0xBFC, "c"),  # Flaps
            (0xEC6, "d"),  # Pressure
            (0x11C6, "d"),  # Mach
            (0x126C, "d"),  # Fuel Weight
            (0x2400, "f"),  # Engine 1 RPM
            (0x2408, "f"),  # Engine 1 Maximum RPM
            (0x2ED0, "f"),  # Angle of Attack
            (0x2ED8, "f"),  # Side Slip Angle
            (0x2EE0, "d"),  # Flight Director
            (0x2EE8, "f"),  # Flight Director Pitch
            (0x2EF0, "f"),  # Flight Director Bank
            (0x3101, "c"),  # Alternator
            (0x3102, "c"),  # Battery
            (0x3103, "c"),  # Avionics Master
            (0x3104, "c"),  # Fuel Pump
            (0x3324, "d"),  # Altitude
            (0x3328, "h"),  # Elevator Axis
            (0x332A, "h"),  # Aileron Axis
            (0x3365, "c"),  # In Menu or Dialog
            (0x6010, "f"),  # Latitude
            (0x6018, "f"),  # Longitude
        ], True)

    while True:
        client.publish(f"/Devices/{hostname}", json.dumps(payload()))
        client.loop()
