##########################
## -- INITIALISATION -- ##
##########################
# Fnctions used for the initialization state in the global script

import sys, csv, time, sys, os, logging
from  pymavlink  import mavutil
sys.path.append("../../")
import ConfigParameters as p


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
			vehicle = mavutil.mavlink_connection(connection_string,  baud=57600)
			vehicle.wait_heartbeat()
			print('\033[92m' + 'CONNECTED TO THE VEHICLE' + '\033[0;0m')
			logger.propagate = False
			logger.info('Connected to the vehicle')
			return vehicle
		except : 
			logger.info('Connextion failed')
			print('\033[95m' + 'No vehicle detected at ' + connection_string + '\033[0;0m')
			connection_string = str(input('Connecting port : '))


def InitialisationVehicle(vehicle, logger) : 
	# This function allows to initialize the vehicle 
	# 		vehicle - object dronekit of the vehicle 
	#		logger - log file 

	## 1- SET THE MODE
	print('\033[93m'+ '>> Setting GUIDED mode ... ' +  '\033[0;0m' )
	logger.info('Setting GUIDED mode')
	vehicle.mav.set_mode_send(vehicle.target_system,
    	mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    	0)
	while True:
		ack_msg = vehicle.recv_match(type='COMMAND_ACK', blocking=True)
		ack_msg = ack_msg.to_dict()
		# Check if command in the same in `set_mode`
		if ack_msg['command'] != mavutil.mavlink.MAVLINK_MSG_ID_SET_MODE:
			continue
		# Print the ACK result !
		print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
		break
	logger.info('MANUAL mode activated')
	print('\033[92m'  + 'MANUAL mode activated !' + '\033[0;0m' )

	## 2 - ARMING 
	print('\033[93m'+ '>> Arming the vehicle ... ' +  '\033[0;0m')
	logger.info('Arming the vehicle')	
	vehicle.mav.command_long_send(
		vehicle.target_system,
		vehicle.target_component,
		mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
		0,
		1, 0, 0, 0, 0, 0, 0)
	vehicle.motors_armed_wait()
	logger.info('Vehicule armed') 
	print('\033[92m'  + 'Vehicle armed !' + '\033[0;0m' )
	return vehicle



def setSpeed(vehicle, speed) : 
	# This function set a speed of the bottom wheels
	vehicle.mav.command_long_send(
		vehicle.target_system, vehicle.target_component,
		mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
		0,            # first transmission of this command
		3 + 8,  # servo instance, offset by 8 MAIN outputs
		2e4*speed, # PWM pulse-width
		0,0,0,0,0     # unused parameters
	)


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


	while True : 
		msg = vehicle.recv_match(type='COMMAND_ACK', blocking=True)
		print(msg)
 			

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

