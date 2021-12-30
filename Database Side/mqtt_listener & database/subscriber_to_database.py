#database.py
import json
import os
from random import seed
import mariadb
import sys
import datetime

# DB Config
DB_Name =  "flightRecord"
username = os.environ.get("username")
password = os.environ.get("password")

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		try:
			self.conn = mariadb.connect(user="aerosim", password="aerosim", host="localhost", database=DB_Name)
			self.conn.commit()
			self.cur = self.conn.cursor()
		except:
			print("Error connecting to MariaDB")
			sys.exit(1)
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Device to DB Table
def Device_Table_Handler(name):	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record("insert into Device (Name) values (?)",[name])
	del dbObj
	print("New device inserted.")
	print("")

# Function to save Session to DB Table
def Session_Table_Handler():
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record("insert into Session (StartTime) values (current_timestamp)")
	del dbObj
	print("New session inserted.")
	print("")

# Function to save SessionDevice to DB Table
def SessionDevice_Table_Handler(deviceId, sessionId):
	#Push into DB Table
	dbObj = DatabaseManager()
	if CheckSessionDevice(deviceId, sessionId) == 0:
		dbObj.add_del_update_db_record("insert into SessionDevice (DeviceId, SessionId) values (?, ?)",[deviceId, sessionId])
	del dbObj
	print("New sessionDevice inserted.")
	print("")

# Function to save Data to DB Table
lastUpdateTime = 0
def Data_Table_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	name = json_Dict['name']
	time_string = json_Dict['time']
	beacon = json_Dict['lights']['beacon']
	landing = json_Dict['lights']['landing']
	strobes = json_Dict['lights']['strobes']
	pitot = json_Dict['pitot']
	ias = json_Dict['ias']
	verticalSpeed = json_Dict['verticalSpeed']
	whiskeyCompass = json_Dict['whiskeyCompass']
	stall = json_Dict['stall']
	overspeed = json_Dict['overspeed']
	slipskid = json_Dict['slipSkid']
	turnrate = json_Dict['turnRate']
	pitch = json_Dict['pitch']
	roll = json_Dict['roll']
	heading = json_Dict['heading']
	autoPilot = json_Dict['autopilot']
	headingSel = json_Dict['headingSel']
	throttleLever = json_Dict['eng1']['throttleLever']
	propellerLever = json_Dict['eng1']['propellerLever']
	magnetOs = json_Dict['eng1']['magnetos']
	rpm = json_Dict['eng1']['rpm']
	maxRpm = json_Dict['eng1']['maxRPM']
	fuelSelector = json_Dict['fuelSelector']
	elevatorTrim = json_Dict['elevatorTrim']
	parkingBrake = json_Dict['parkingBrake']
	landingGear = json_Dict['landingGear']
	flaps = json_Dict['flaps']
	pressure = json_Dict['pressure']
	mach = json_Dict['mach']
	fuelWeight = json_Dict['fuelWeight']
	aoa = json_Dict['aoa']
	sideSlip = json_Dict['sideSlip']
	flightDirector = json_Dict['flightDirector']
	flightDirectorPitch = json_Dict['flightDirectorPitch']
	flightDirectorBank = json_Dict['flightDirectorBank']
	alternator = json_Dict['alternator']
	battery = json_Dict['battery']
	avionics = json_Dict['avionics']
	fuelPump = json_Dict['fuelPump']
	altitude = json_Dict['altitude']
	elevatorAxis = json_Dict['elevatorAxis']
	aileronAxis = json_Dict['aileronAxis']
	latitude = json_Dict['latitude']
	longitude = json_Dict['longitude']
	status = json_Dict['status']

	#Parse data
	time = datetime.datetime.strptime(str(datetime.datetime.now().year) + " " + time_string, '%Y %m/%d %H:%M:%S')
	sessionId = GetSessionId()
	deviceId = GetDeviceId(name)
	
	
	#Push into DB Table
	#Only Update once per delta time
	dbObj = DatabaseManager()
	SessionDevice_Table_Handler(deviceId, sessionId)
	dbObj.add_del_update_db_record("insert into Data (DeviceId, SessionId, time, beacon, landing, strobes, pitot, ias, verticalSpeed, whiskeyCompass, stall, overspeed, slipskid, turnrate, pitch, roll, heading, autoPilot, headingSel, throttleLever, propellerLever, magnetOs, rpm, maxRpm, fuelSelector, elevatorTrim, parkingBrake, landingGear, flaps, pressure, mach, fuelWeight, aoa, sideSlip, flightDirector, flightDirectorPitch, flightDirectorBank, alternator, battery, avionics, fuelPump, altitude, elevatorAxis, aileronAxis, latitude, longitude, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(deviceId, sessionId, time, beacon, landing, strobes, pitot, ias, verticalSpeed, whiskeyCompass, stall, overspeed, slipskid, turnrate, pitch, roll, heading, autoPilot, headingSel, throttleLever, propellerLever, magnetOs, rpm, maxRpm, fuelSelector, elevatorTrim, parkingBrake, landingGear, flaps, pressure, mach, fuelWeight, aoa, sideSlip, flightDirector, flightDirectorPitch, flightDirectorBank, alternator, battery, avionics, fuelPump, altitude, elevatorAxis, aileronAxis, latitude, longitude, status,))
	del dbObj
	print("New data inserted.")
	print("")


#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
	if "Devices" in Topic:
		Data_Table_Handler(jsonData)

#===============================================================

#Helper functions

#Check if a device exists in Device table
def CheckDevice(name):
	dbObj = DatabaseManager()
	dbObj.cur.execute("select exists(select * from Device where Name = ?)", (name,))
	result_singleton = dbObj.cur.fetchall()
	for row in result_singleton:
		result = row[0]
	return result
	
#Find DeviceId
def GetDeviceId(name):
	if CheckDevice(name) == 0:
		Device_Table_Handler(name)
	dbObj = DatabaseManager()
	dbObj.cur.execute("select DeviceId from Device where Name = ? limit 1", (name,))
	DeviceId_singleton = dbObj.cur.fetchall()
	for row in DeviceId_singleton:
		DeviceId = row[0]
	return DeviceId

#Find SessionId
isNewSession = True
def GetSessionId():
	global isNewSession
	if isNewSession:
		Session_Table_Handler()
		isNewSession = False
	dbObj = DatabaseManager()
	dbObj.cur.execute("select max(SessionId) from Session")
	SessionId_singleton = dbObj.cur.fetchall()
	for row in SessionId_singleton:
		SessionId = row[0]
	return SessionId

#Check if a deviceId is in SessionDevice table
def CheckSessionDevice(deviceId, sessionId):
	dbObj = DatabaseManager()
	dbObj.cur.execute("select exists(select * from SessionDevice where DeviceId = ? AND SessionId = ? limit 1)", (deviceId, sessionId,))
	result_singleton = dbObj.cur.fetchall()
	for row in result_singleton:
		result = row[0]
	return result

