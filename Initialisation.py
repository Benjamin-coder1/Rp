##########################
## -- INITIALISATION -- ##
##########################
# Fnctions used for the initialization state in the global script

import csv, time, sys, os, logging
import  dronekit  
import Parameters as p


def setup_logger(logFileInfo):
    # This function allows to create as many log file as we want 
	#		logFileInfo - Information about the log file    format / dateFormat/name/level
	formatter = logging.Formatter(logFileInfo['format'], datefmt=logFileInfo['dateFormat'])
	handler = logging.FileHandler(logFileInfo['name'])        
	handler.setFormatter(formatter)
	logger = logging.getLogger(logFileInfo['name'].split('.')[0])
	logger.setLevel(logFileInfo['level'])
	logger.addHandler(handler)
	return logger

# File loggers
Events = setup_logger(p.logFileEvent)
Values = setup_logger(p.logFileValue)


def getConnexionVehicle(connection_string, logger) : 
	# This function establishes the connexion with the true vehicle
	# 	connection_string - identification of the connexion between the computer and the vehicle
	# 	logger - logger for log file
	 
	# Connect to the Vehicle.
	logger.info('Connexion with the vehicle on %s', connection_string )
	print("Connecting to vehicle on : %s" % (connection_string,))
	while True : 
		try : 
			print('\033[93m' + '>> CONNEXION VEHICLE ... ' + '\033[0;0m')
			vehicle = dronekit.connect(connection_string, wait_ready=True, baud=57600)
			print('\033[92m' + 'CONNECTED TO THE VEHICLE' + '\033[0;0m')
			logger.propagate = False
			logger.info('Connected to the vehicle')
			return vehicle
		except : 
			logger.info('Connextion failed')
			print('\033[95m' + 'No vehicle detected at ' + connection_string + '\033[0;0m')
			connection_string = str(input('Connecting port : '))


def InitialisationVehicle(vehicle, fileName, logger) : 
	# This function allows to initialize the vehicle 
	# 		vehicle - object dronekit of the vehicle 
	#		logger - log file 

	## 1- ARMING THE VEHICLE 
	print('\033[93m'+ '>> Arming the vehicle ... ' +  '\033[0;0m')
	logger.info('Arming the vehicle')	
	while not vehicle.armed :
		vehicle.armed = True
		time.sleep(1)
	logger.info('Vehicule armed') 
	print('\033[92m'  + 'Vehicle armed !' + '\033[0;0m' )

	## 2 - SETTING THE PARAMETERS
	vehicle = setParameters(vehicle, fileName, logger)
	time.sleep(10)

	## 3 - SETTING GUIDED THE MODE
	print('\033[93m'+ '>> Setting GUIDED mode ... ' +  '\033[0;0m' )
	logger.info('Setting GUIDED mode')
	while not vehicle.mode.name=='GUIDED' :
		vehicle.mode = dronekit.VehicleMode("GUIDED")
		time.sleep(1)
	logger.info('GUIDED mode activated')
	print('\033[92m'  + 'GUIDED mode activated !' + '\033[0;0m' )


	return vehicle


def setParameters(vehicle, fileName, logger) : 
	# This function take a vehicle and a CSV list of parameters to initialise
	# 	vehicle - object dronkit 
	# 	fileName - file CSV with the shape   "value;name"
	# 	logger - logger for log file

	# Testing the file 
	while True : 
		try : 			
			file = open(fileName)
			break
		except : 
			print('\033[95m' + 'File of parameters unknow' + '\033[0;0m')
			logger.error('File of parameters unknow "%s"', fileName)
			fileName = str(input('CSV file name : '))

	new_value_dic = {}
	myReader = csv.reader(file, delimiter=';')
	for row in myReader :		
		new_value_dic[row[1]] = float(row[0])	

	print('\033[93m' + '>> SETTING PARAMETERS ... ' + '\033[0;0m')
	up = [0, 0, 0, 0]
	for name, value in new_value_dic.items() :		
		if name in vehicle.parameters.keys() : 	
			attempt = 0
			while attempt < 10 and vehicle.parameters[name] != value : 
				vehicle.parameters[name] = value
				attempt += 1
				time.sleep(1/2)	
			
			if attempt == 0 : 	up[0] += 1  #already set up
			elif attempt > 0 and attempt < 10 :  up[1] += 1  #set up
			else :	up[2] += 1  #fail 

			percent = str(round(10000*up[3]/len(new_value_dic))/100) 
			sys.stdout.write("\r{0}".format(" "*50))
			sys.stdout.write("\r{0}".format("[ " + str(percent) + "% ] " + name + " : " + str(value)) )
			sys.stdout.flush()
			time.sleep(0.1)		
			logger.info("%s : %f",  str(name), value )
		up[3] += 1

	print('\033[92m' + 'Initialization completed with : ' + '\033[0;0m')
	print(str(up[0]) + ' parameters already set up')
	print(str(up[1]) + ' parameters set up')
	print(str(up[2]) + ' parameters failed')
	logging.info( str(up[0]) + ' parameters already set up / ' + str(up[1]) + ' parameters set up / ' + str(up[2]) + ' parameters failed')
	return vehicle



def setValue(vehicle): 
	# Function that reads the phisical values of the vehicle and save it with the shape: 
	# Time;yaw;pitch;roll;lon;lat;alt
    modeStates = {'MANUAL':0, 'ACRO':1, 'STEERING':2, 'HOLD':3, 'LOITER':4, 'FOLLOW':5, 'SIMPLE':6, 'AUTO':7, 'RTL':8, 'SMARTRTL':9, 'GUIDED':10}
    systemStates = {'UNINIT':0, 'BOOT':1, 'CALIBRATING':2, 'STANDBY':3, 'ACTIVE':4, 'CRITICAL':5, 'EMERGENCY':6, 'POWEROFF':7}
    global state
    print('Start of saving measurements in log file')
    Events.info('Start of saving measurements in log file')	
    headers = 'eph' + \
            ';' + 'epv' + \
            ';' + 'fix_type' + \
            ';' + 'satellites'  + \
            ';' + 'gps_status' + \
            ';' + 'ekf' + \
            ';' + 'latitude' + \
            ';' + 'longitude' + \
            ';' + 'altitude' + \
            ';' + 'north' + \
            ';' + 'east' + \
            ';' + 'down' + \
            ';' + 'pitch' + \
            ';' + 'yaw' + \
            ';' + 'roll' + \
            ';' + 'Vx' + \
            ';' + 'Vy' + \
            ';' + 'Vz' + \
            ';' + 'groundspeed' + \
            ';' + 'voltage' + \
            ';' + 'current' + \
            ';' + 'power' + \
            ';' + 'last_heartbeat' + \
            ';' + 'armed' + \
            ';' + 'mode' + \
            ';' + 'armable' + \
            ';' + 'system_status'
    Events.info(headers)
    while p.state > 1 :
        mode = modeStates.get(vehicle.mode.name)
        sys_status = systemStates.get(vehicle.system_status.state)
        info = str(vehicle.gps_0.eph) + \
			';' + str(vehicle.gps_0.epv) + \
			';' + str(vehicle.gps_0.fix_type) + \
			';' + str(vehicle.gps_0.satellites_visible) + \
        	';' + str(vehicle.gps_0) + \
			';' + str(int(vehicle.ekf_ok)) + \
			';' + str(vehicle.location.global_frame.lat) + \
			';' + str(vehicle.location.global_frame.lon) + \
			';' + str(vehicle.location.global_frame.alt) + \
			';' + str(vehicle.location.local_frame.north) + \
			';' + str(vehicle.location.local_frame.east) + \
			';' + str(vehicle.location.local_frame.down) + \
            ';' + str(vehicle.attitude.pitch) + \
			';' + str(vehicle.attitude.yaw) + \
			';' + str(vehicle.attitude.roll) + \
			';' + str(vehicle.velocity[0]) + \
			';' + str(vehicle.velocity[1]) + \
			';' + str(vehicle.velocity[2]) + \
			';' + str(vehicle.groundspeed) + \
			';' + str(vehicle.battery.voltage) + \
			';' + str(vehicle.battery.current) + \
        	';' + str(vehicle.battery.level) + \
			';' + str(vehicle.last_heartbeat) + \
			';' + str(int(vehicle.armed)) + \
			';' + str(int(vehicle.is_armable)) + \
			';' + str(mode) + \
			';' + str(sys_status) 
        info = ((info.replace('None', '-1')).replace('GPSInfo:fix=', '')).replace('num_sat=', '') 
        Values.info(info)
        time.sleep(1/p.sensorFrequency)


def StopFromQgc(vehicle) : 
	# This function allows to stop the autonomous mode when we get a text from QGC 
	#       connexion_string - link to listen communication 
	global state 	
	Events.info('Starting listening to Qgc')

	# Method for when we receive the text
	def my_method(self, name, msg):
		global state 
		if  msg.command == 203 or vehicle.mode.name == "GUIDED": 	
			print("Command received from the Gound station, switching mode ...")
			Events.info('Command received from the Gound station, switching mode')
			vehicle.mode = dronekit.VehicleMode("GUIDED")
			p.state = 2

	# Listener 
	vehicle.add_message_listener('COMMAND_ACK',my_method)
	while p.state == 3 :	
		time.sleep(1)
	vehicle.remove_message_listener('COMMAND_ACK',my_method)

