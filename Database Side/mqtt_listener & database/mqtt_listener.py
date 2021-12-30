#mqtt_listener.py
import paho.mqtt.client as mqtt
from subscriber_to_database import sensor_Data_Handler

# MQTT Settings 
MQTT_Broker = "192.168.0.128"		#???
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "/Devices/#"

#Subscribe to all device at Base Topic
def on_connect(mosq, obj, rc, a):
	mqttc.subscribe(MQTT_Topic, 0)

#Save Data into DB Table
def on_message(mosq, obj, msg):
	# This is the Master Call for saving MQTT Data into DB
	print("MQTT Data Received...")
	print("MQTT Topic: " + msg.topic)
	sensor_Data_Handler(msg.topic, msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
mqttc.loop_forever()