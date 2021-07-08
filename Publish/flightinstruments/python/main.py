#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import math
import sys

import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtSvg, QtWidgets

from qfi import qfi_ADI, qfi_ALT, qfi_HSI, qfi_SI, qfi_TC, qfi_VSI
from threadGUI import ThreadGUI


class MqttClient(QtCore.QObject):
    Disconnected = 0
    Connecting = 1
    Connected = 2

    MQTT_3_1 = mqtt.MQTTv31
    MQTT_3_1_1 = mqtt.MQTTv311

    connected = QtCore.pyqtSignal()
    disconnected = QtCore.pyqtSignal()

    stateChanged = QtCore.pyqtSignal(int)
    hostnameChanged = QtCore.pyqtSignal(str)
    portChanged = QtCore.pyqtSignal(int)
    keepAliveChanged = QtCore.pyqtSignal(int)
    cleanSessionChanged = QtCore.pyqtSignal(bool)
    protocolVersionChanged = QtCore.pyqtSignal(int)

    messageSignal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(MqttClient, self).__init__(parent)

        self.m_hostname = ""
        self.m_port = 1883
        self.m_keepAlive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = MqttClient.MQTT_3_1

        self.m_state = MqttClient.Disconnected

        self.m_client = mqtt.Client(clean_session=self.m_cleanSession,
                                    protocol=self.protocolVersion)

        self.m_client.on_connect = self.on_connect
        self.m_client.on_message = self.on_message
        self.m_client.on_disconnect = self.on_disconnect

    @QtCore.pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self.m_state

    @state.setter
    def state(self, state):
        if self.m_state == state:
            return
        self.m_state = state
        self.stateChanged.emit(state)

    @QtCore.pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self.m_hostname

    @hostname.setter
    def hostname(self, hostname):
        if self.m_hostname == hostname:
            return
        self.m_hostname = hostname
        self.hostnameChanged.emit(hostname)

    @QtCore.pyqtProperty(int, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port == port:
            return
        self.m_port = port
        self.portChanged.emit(port)

    @QtCore.pyqtProperty(int, notify=keepAliveChanged)
    def keepAlive(self):
        return self.m_keepAlive

    @keepAlive.setter
    def keepAlive(self, keepAlive):
        if self.m_keepAlive == keepAlive:
            return
        self.m_keepAlive = keepAlive
        self.keepAliveChanged.emit(keepAlive)

    @QtCore.pyqtProperty(bool, notify=cleanSessionChanged)
    def cleanSession(self):
        return self.m_cleanSession

    @cleanSession.setter
    def cleanSession(self, cleanSession):
        if self.m_cleanSession == cleanSession:
            return
        self.m_cleanSession = cleanSession
        self.cleanSessionChanged.emit(cleanSession)

    @QtCore.pyqtProperty(int, notify=protocolVersionChanged)
    def protocolVersion(self):
        return self.m_protocolVersion

    @protocolVersion.setter
    def protocolVersion(self, protocolVersion):
        if self.m_protocolVersion == protocolVersion:
            return
        if protocolVersion in (MqttClient.MQTT_3_1, MQTT_3_1_1):
            self.m_protocolVersion = protocolVersion
            self.protocolVersionChanged.emit(protocolVersion)

    #################################################################
    @QtCore.pyqtSlot()
    def connectToHost(self):
        if self.m_hostname:
            self.m_client.connect(self.m_hostname,
                                  port=self.port,
                                  keepalive=self.keepAlive)

            self.state = MqttClient.Connecting
            self.m_client.loop_start()

    @QtCore.pyqtSlot()
    def disconnectFromHost(self):
        self.m_client.disconnect()

    def subscribe(self, path):
        if self.state == MqttClient.Connected:
            self.m_client.subscribe(path)

    #################################################################
    # callbacks
    def on_message(self, mqttc, obj, msg):
        # mstr = msg.payload.decode("ascii")
        mstr = json.loads(msg.payload)
        #print("on_message", mstr, obj, mqttc)
        self.messageSignal.emit(mstr)

    def on_connect(self, *args):
        #print("on_connect", args)
        self.state = MqttClient.Connected
        self.connected.emit()

    def on_disconnect(self, *args):
        #print("on_disconnect", args)
        self.state = MqttClient.Disconnected
        self.disconnected.emit()


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.layout = QtWidgets.QGridLayout()

        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.resize(240, 240)
        self.adi.reinit()
        self.layout.addWidget(self.adi, 0, 0)

        self.alt = qfi_ALT.qfi_ALT(self)
        self.alt.resize(240, 240)
        self.alt.reinit()
        self.layout.addWidget(self.alt, 0, 1)

        self.hsi = qfi_HSI.qfi_HSI(self)
        self.hsi.resize(240, 240)
        self.hsi.reinit()
        self.layout.addWidget(self.hsi, 1, 0)

        self.si = qfi_SI.qfi_SI(self)
        self.si.resize(240, 240)
        self.si.reinit()
        self.layout.addWidget(self.si, 1, 1)

        self.vsi = qfi_VSI.qfi_VSI(self)
        self.vsi.resize(240, 240)
        self.vsi.reinit()
        self.layout.addWidget(self.vsi, 2, 0)

        self.tc = qfi_TC.qfi_TC(self)
        self.tc.resize(240, 240)
        self.tc.reinit()
        self.layout.addWidget(self.tc, 2, 1)

        self.setLayout(self.layout)

        self.show()

        self.client = MqttClient(self)
        self.client.stateChanged.connect(self.on_stateChanged)
        self.client.messageSignal.connect(self.on_messageSignal)

        self.client.hostname = "aerosimmqtt.eastasia.azurecontainer.io"
        self.client.connectToHost()

    @QtCore.pyqtSlot(int)
    def on_stateChanged(self, state):
        if state == MqttClient.Connected:
            print(state)
            self.client.subscribe("/Sensor/ModelA")

    @QtCore.pyqtSlot(dict)
    def on_messageSignal(self, msg):
        roll = msg["Roll"] * 360 / (65536*65536)*(-1)
        pitch = msg["Pitch"] * 360 / (65536*65536)*(-1)
        speed = msg["IAS"] / 128 * 463/900
        heading = msg["Heading"] * 360 / (65536*65536)
        altitude = msg["Altitude"]
        vertical_speed = msg["Vertical Speed"] * 60*3.28084/256
        self.adi.setRoll(roll)
        self.adi.setPitch(pitch)
        self.si.setSpeed(speed)
        self.hsi.setHeading(heading)
        self.vsi.setClimbRate(vertical_speed)
        self.alt.setAltitude(altitude)
        # self.tc.setTurnRate(10*math.cos(val))
        # self.tc.setSlipSkid(10*math.cos(val))
        self.adi.viewUpdate.emit()
        self.alt.viewUpdate.emit()
        self.si.viewUpdate.emit()
        self.hsi.viewUpdate.emit()
        self.vsi.viewUpdate.emit()
        # self.tc.viewUpdate.emit()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()

    t2 = ThreadGUI(widget)
    t2.daemon = True
    t2.start()

    sys.exit(app.exec_())
