import mysql_operate as mysql


class MqttToDb(object):

    def __init__(self, is_record=None, session_id=None):
        self._is_record = is_record
        self._session_id = session_id

    # is_record getter setter
    @property
    def is_record(self):
        print(self._is_record)
        return self._is_record

    @is_record.setter
    def is_record(self, new_is_record):
        self._is_record = new_is_record

    # session_id getter setter
    @property
    def session_id(self):
        print('get session_id')
        return self._session_id

    @session_id.setter
    def session_id(self, new_session_id):
        print('set session_id')
        self._session_id = new_session_id

    def payload_to_db(self, dict):
        name = dict['name']
        time = dict['time']
        navigation = dict['lights']['navigation']
        beacon = dict['lights']['beacon']
        landing = dict['lights']['landing']
        taxi = dict['lights']['taxi']
        strobes = dict['lights']['strobes']
        pitot = dict['pitot']
        ias = dict['ias']
        verticalSpeed = dict['verticalSpeed']
        whiskeyCompass = dict['whiskeyCompass']
        stall = dict['stall']
        overspeed = dict['overspeed']
        slipSkid = dict['slipSkid']
        turnRate = dict['turnRate']
        pitch = dict['pitch']
        roll = dict['roll']
        heading = dict['heading']
        autopilot = dict['autopilot']
        headingSel = dict['headingSel']
        altitudeSel = dict['altitudeSel']
        airspeedSel = dict['airspeedSel']
        throttleLever = dict['eng1']['throttleLever']
        propellerLever = dict['eng1']['propellerLever']
        mixtureLever = dict['eng1']['mixtureLever']
        magnetos = dict['eng1']['magnetos']
        rpm = dict['eng1']['rpm']
        maxRPM = dict['eng1']['maxRPM']
        fuelSelector = dict['fuelSelector']
        elevatorTrim = dict['elevatorTrim']
        parkingBrake = dict['parkingBrake']
        landingGear = dict['landingGear']
        flaps = dict['flaps']
        pressure = dict['pressure']
        mach = dict['mach']
        fuelWeight = dict['fuelWeight']
        aoa = dict['aoa']
        sideSlip = dict['sideSlip']
        flightDirector = dict['flightDirector']
        flightDirectorPitch = dict['flightDirectorPitch']
        flightDirectorBank = dict['flightDirectorBank']
        alternator = dict['alternator']
        battery = dict['battery']
        avionics = dict['avionics']
        fuelPump = dict['fuelPump']
        altitude = dict['altitude']
        elevatorAxis = dict['elevatorAxis']
        aileronAxis = dict['aileronAxis']
        latitude = dict['latitude']
        longitude = dict['longitude']
        status = dict['status']

        device_id = name.split("-")[1]

        sql = f"INSERT INTO data VALUES(NULL, {self.session_id, device_id, time, navigation, beacon, landing, taxi, strobes, pitot, ias, verticalSpeed, whiskeyCompass, stall, overspeed, slipSkid, turnRate, pitch, roll, heading, autopilot, headingSel, altitudeSel, airspeedSel, throttleLever, propellerLever, mixtureLever, magnetos, rpm, maxRPM, fuelSelector, elevatorTrim, parkingBrake, landingGear, flaps, pressure, mach, fuelWeight, aoa, sideSlip, flightDirector, flightDirectorPitch, flightDirectorBank, alternator, battery, avionics, fuelPump, altitude, elevatorAxis, aileronAxis, latitude, longitude, status})"
        print(sql)
        mysql.db.execute_db(sql)
        


client = MqttToDb(False, 0)
