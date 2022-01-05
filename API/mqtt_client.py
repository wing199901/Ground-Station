import paho.mqtt.client as mqtt
from mqtt_config import *


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC, qos=0)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


if __name__ == "__main__":
    client = mqtt.Client()

# Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message

# Connect to the Broker
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

    client.loop_forever()
