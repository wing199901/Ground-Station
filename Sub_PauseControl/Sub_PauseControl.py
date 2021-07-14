import paho.mqtt.client as mqtt
from fsuipc import FSUIPC


# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/Sensor/ModelA/PauseControl")


# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode('utf-8'))
    # return msg.payload.decode('utf-8')
    message = msg.payload.decode('utf-8')

    PauseControl(message)
    return msg.payload.decode('utf-8')


def on_disconnect(client, userdata, rc=0):
    logging.debug("DisConnected result code " + str(rc))
    client.loop_stop()

def PauseControl(msg):
    #TESTING
    print(type(msg))
    try:
        if msg == "!pause":
            print("Pause the Game.")
            PauseAndUnPause(True)

        elif msg == "!unpause":
            print("Continue the Game.")
            PauseAndUnPause(False)

        else:
            print("This is not Pause Control.")

    except Exception as e:
        print(e)


def PauseAndUnPause(Pause):
    # This python is used to Read the Pause Control signal only (for test)
    with FSUIPC() as fsuipc:

        # msg = input("P = Pause, U = Unpause:\n") #test
        if Pause == True:
            try:
                fsuipc.write([(0x262, "H", 1)])
                print("Pause!!!")
            except Exception as e:
                print(e)

        elif Pause == False:
            try:
                fsuipc.write([(0x262, "H", 0)])
                print("UnPause!!!")
            except Exception as e:
                print(e)

        else:
            print("Unexpected Error?")


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.username_pw_set("try","xxxx")
    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("192.168.0.128", 1883, 60)

    client.loop_start()
    print("START!")
    while True:
        client.on_message = on_message
