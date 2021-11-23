# Ground Station - a flight monitor for flight simulators
## Using MQTT as the main protocol
[![](https://i1.wp.com/randomnerdtutorials.com/wp-content/uploads/2020/10/ESP8266-NodeMCU-Overview-MQTT-Publish-BME680-Temperature-Humidity-Pressure-Gas-Readings.png?w=862&quality=100&strip=all&ssl=1)](https://i1.wp.com/randomnerdtutorials.com/wp-content/uploads/2020/10/ESP8266-NodeMCU-Overview-MQTT-Publish-BME680-Temperature-Humidity-Pressure-Gas-Readings.png?w=862&quality=100&strip=all&ssl=1)
## MQTT Broker
We use [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto "eclipse-mosquitto") as Broker
### Quickstart
1. SSH to Raspberry Pi:
```bash
 ssh ubuntu@192.168.0.128
```
2. Login to Raspberry Pi:
```bash
The Login name is 'ubuntu'
Password is stick on the Pi, It locate on my table
```
3. Docker run:
```bash
docker run -d -p 1883:1883 eclipse-mosquitto:1.6.15
```
3. Done.

## Publish Side (P3D)
You can find files in Publish folder. To build it, you need a Windows machine.
### Quickstart
1. Install [PyInstaller](https://www.pyinstaller.org/ "PyInstaller") from PyPI on a Windows machine:
```bash
pip install pyinstaller
```
2. Build publish.exe:
```bash
pyinstaller -F Ground-Station/Publish/publish.py
```
3. If you don't want to build it:
```
You can find an existing .exe in Ground-Station/Publish/dist/
```
4. Copy it to Console 40 or Model A.
5. Run the .exe

## Subscribe Side (Ground Station)
You can find files in root folder. To Open this Qt project, you need to install Qt5 into your system first.

We are using **Qt 5.12.11** as our main development version. In order to use MQTT in Qt, you need to install **qtmqtt** to your system manually. You can find install files in the below link:
```
https://github.com/qt/qtmqtt/tree/5.12.11
```
Tutorial for Windows:
```
https://blog.csdn.net/luoyayun361/article/details/104671603
```
Tutorial for macOS:
```
https://blog.csdn.net/yc__coder/article/details/106956760
```
### Quickstart
To open project at Qt, just double click **Ground-Station.pro**.

### User Guide
![image](https://user-images.githubusercontent.com/13567466/142921195-85bce5e2-ce6a-47f6-92ac-deebd7c7e96f.png)

1. Press 'MQTT' tab on the menu bar, then press 'connect' and 'subscribe'.
2. You can find more control at the 'Control' tab.

### File Sturct
![螢幕截圖 2021-11-23 03 16 39](https://user-images.githubusercontent.com/13567466/142922249-21d1d7ff-1ae1-479f-b8d8-154c228acdfa.png)


## Target
- Runs on macOS or Windows
- Simply unzip and run – no installation required
- OpenStreetMaps interface
- Support for Prepar3D 5
- PFD, MFD and Fuel panel with aircraft-specific details
- Full logbook of flights, with many reports
- PDF chart viewer
- English language
- Much more
