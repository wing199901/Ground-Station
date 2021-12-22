#Import libraries, mariadb, and sys
import mariadb
from mariadb import Error as e
import sys


# Attempt connection to Mariadb,
try:
    conn = mariadb.connect(
        user="aerosim",
        password="aerosim",
        host="localhost", #Localhost-> for raspberry Pi use server address if use server online server in the fut
        port=3306,        #Default port for mariaDB is 3306
        database="flightRecord"
    )
#Exception error, try to connect to MariaDB, print failure message if dosen't connect
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


#Generate connection cursor, used to control and execute statements
cur = conn.cursor()


#Create 4 Tables, Device, Session, SessionDevice and CreateData in sequence, SessionDevice and Data uses SessionID and DeviceID as foreign Keys


CreateDevice="""                   
create table Device ( DeviceId INTEGER AUTO_INCREMENT, Name TEXT, PRIMARY KEY(DeviceId) );
"""

CreateSession="""                   
create table Session (
    SessionID INTEGER AUTO_INCREMENT,
	StartTime DATETIME,
	PRIMARY KEY(SessionID)
);
"""

CreateSessionDevice = """
create table SessionDevice(     
    SessionId INTEGER,     
    DeviceId INTEGER,    
    FOREIGN KEY(DeviceId) REFERENCES Device(DeviceId),     
    FOREIGN KEY(SessionId) REFERENCES Session(SessionId)
);
"""



CreateData="""                   
create table Data (
  Id              INTEGER AUTO_INCREMENT,
  SessionId       integer,
  DeviceId        integer,
  time            DATETIME,
  beacon          BOOL,
  landing         BOOL,
  strobes         BOOL,
  pitot           BOOL,
  ias             FLOAT,
  verticalSpeed   FLOAT,
  whiskeyCompass  DOUBLE,
  stall           BOOLEAN,
  overspeed       BOOLEAN,
  slipskid        INT,
  turnrate        FLOAT,
  roll            DOUBLE,
  heading         DOUBLE,
  pitch           DOUBLE,
  autopilot       BOOLEAN,
  headingSel      DOUBLE,
  throttleLever   DOUBLE,
  propellerLever  INTEGER,
  magnetOs        INTEGER,
  rpm             FLOAT,
  maxRpm          DOUBLE,
  fuelSelector    INTEGER,
  elevatorTrim    FLOAT,
  parkingBrake    BOOLEAN,
  landingGear     BOOLEAN,
  flaps           INT,
  pressure        FLOAT,
  mach            FLOAT,
  fuelWeight 	    DOUBLE,
  aoa             DOUBLE,
  sideSlip        DOUBLE,
  flightDirector  BOOLEAN,
  flightDirectorPitch INT,
  flightDirectorBank  INT,
  alternator      BOOLEAN,
  battery         BOOLEAN,
  avionics        BOOLEAN,
  fuelPump        BOOLEAN,
  altitude 	      INTEGER,
  elevatorAxis    INTEGER,
  aileronAxis     INTEGER,
  latitude        DOUBLE,
  longitude       DOUBLE,
  status          TEXT,
  PRIMARY KEY(Id),
  FOREIGN KEY(SessionId) REFERENCES Session(SessionId),
  FOREIGN KEY(DeviceId) REFERENCES Device(DeviceId)
);
"""
# Try to execute the clauses in mysql, they have to be separated since one statement containing all of the clause will give error
try:
    cur.execute(CreateDevice)
    cur.execute(CreateSession)
    cur.execute(CreateSessionDevice)
    cur.execute(CreateData)

    # Outputs successful message if tables are created
    print("Tables have been created successfully")

#Displays the exception error if there is a failure

except mariadb.Error as e:
    print(f"Error: {e}")


#Close DB
cur.close()
conn.close()