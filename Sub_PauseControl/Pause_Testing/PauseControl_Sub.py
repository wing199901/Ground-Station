import json

import paho.mqtt.client as mqtt
from fsuipc import FSUIPC

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時
    # 地端程式將會重新訂閱
    client.subscribe("/")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):          
    print(msg.topic+" "+ msg.payload.decode('utf-8'))
    # return msg.payload.decode('utf-8')
    message = msg.payload.decode('utf-8')

    # for testing only
    print(type(message))
    jsonMsg = json.loads(message)
    print(type(jsonMsg))
    print(jsonMsg["0x262"])

    # Pause control (write 1 to pause, 0 to un-pause).
    if jsonMsg["0x262"] == True:
        print("Pause the Game.")
        with FSUIPC() as fsuipc:
            prepared = fsuipc.prepare_data([
                jsonMsg
            ], True)
        while True:
            prepared = prepared.write

    elif jsonMsg["0x262"] == False:
        print("Unpause the Game.")
        with FSUIPC() as fsuipc:
            prepared = fsuipc.prepare_data([
            ("0x262",False)
            ], True)
        while True:
            prepared = prepared.write
                
    else:
        print("This is not Pause Control.")


def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))
    client.loop_stop()

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.username_pw_set("try","xxxx")
    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("192.168.0.128", 1883, 60)

    client.loop_start()

    while True:
        client.on_message = on_message
        # print(data)






