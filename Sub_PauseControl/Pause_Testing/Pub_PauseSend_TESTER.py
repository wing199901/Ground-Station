import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時
    # 地端程式將會重新訂閱
    topic = "/Sensor/ModelA/PauseControl"
    client.subscribe(topic)
    print("Connecting to topic: ", topic)
    input("Press Enter to continue...")
# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    print(msg.topic + " " + msg.payload.decode('utf-8'))

client = mqtt.Client()
client.on_connect = on_connect
# 設定連線資訊(IP, Port, 連線時間)
client.connect("192.168.0.128", 1883, 60)

while True:
    msg = input("INPUT\n")
    if  msg == "A":
        client.publish("/Sensor/ModelA/PauseControl", "1111TESTING")
    elif msg == "p":
        client.publish("/Sensor/ModelA/PauseControl", "!pause")
    elif msg == "unp":
        client.publish("/Sensor/ModelA/PauseControl", "!unpause")
    else:
        client.publish("/Sensor/ModelA/PauseControl", "2222TESTING")

client.loop_forever()