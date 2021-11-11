##########################
## -- INITIALISATION -- ##
##########################
# Fnctions used for the initialization state in the global script

import csv, time, sys, os, logging
from pymavlink import mavutil
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
			vehicle = mavutil.mavlink_connection(connection_string, wait_ready=True, baud=57600)
			print('\033[92m' + 'CONNECTED TO THE VEHICLE' + '\033[0;0m')
			logger.propagate = False
			logger.info('Connected to the vehicle')
			return vehicle
		except Exception as e : 
			logger.info('Connextion failed')
			print('\033[95m' + str(e.args) + '\033[0;0m')
			connection_string = str(input('Connecting port : '))


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



vehicle = getConnexionVehicle('/dev/ttyUSB0', Events)
# setParameters(vehicle, 'vehicleParameters.csv', Values)