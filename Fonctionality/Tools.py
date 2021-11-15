import sys, time, logging
import pyrealsense2 as rs 


def CreateLogger(logFileInfo):
	"""This function allows to create as many log file as we want 
		logFileInfo - Information about the log file    format / dateFormat/name/level"""
	formatter = logging.Formatter(logFileInfo['format'], datefmt=logFileInfo['dateFormat'])
	handler = logging.FileHandler(logFileInfo['name'])        
	handler.setFormatter(formatter)
	logger = logging.getLogger(logFileInfo['name'].split('.')[0])
	logger.setLevel(logFileInfo['level'])
	logger.addHandler(handler)
	return logger


def ConnectCamera(logger=False) : 
	""" This function create a connexion with the camera set logger to write what append in the 
	log file """
	pipe, align, cfg = [rs.pipeline() , rs.align(rs.stream.color), rs.config()]
	while True : 
		try:
			print('Connexion realsense Camera ... ')
			if logger != False : 
				logger.info("Connexion realsense Camera")
			cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
			cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
			pipe.start(cfg)
			print('\033[92m' + 'Camera configurated and connected.' + '\033[0m')  
			if logger != False : 
				logger.info("Camera configurated and connected")   
			return pipe, align 
		except Exception as e:
			print('\033[91m' + str(e.args) + '\033[0m') 
			if logger != False : 
				logger.info(str(e.args) )       
			for tm in range(30) : 
				sys.stdout.write("\r{0}".format(" "*20))
				sys.stdout.write("\r{0}".format("Reconnection attempt in " + str(30 - tm) + " s ...", 10))
				sys.stdout.flush()
				time.sleep(1)

def disp( msg, color=-1,  logger=False) : 
	""" This function print colored msg and can send it to a logfile """ 
	if logger != False : 
		logger.info(msg)
	
	if color == 0 : 
		# RED 
		colorMsg = '\033[95m'
	elif color == 1 : 
		# GREEN 
		colorMsg = '\033[92m'
	elif color == 2 : 
		# YELLOW 
		colorMsg = '\033[93m'
	elif color == 3 : 
		# BLUE 
		colorMsg =  '\033[94m' 
	elif color == 4 : 
		# WHITE 
		print(msg)
		return 
	else : 
		# No print 
		return 
	print( colorMsg + msg + '\033[0;0m')







# def setValue(vehicle): 
# 	# Function that reads the phisical values of the vehicle and save it with the shape: 
# 	# Time;yaw;pitch;roll;lon;lat;alt
#     modeStates = {'MANUAL':0, 'ACRO':1, 'STEERING':2, 'HOLD':3, 'LOITER':4, 'FOLLOW':5, 'SIMPLE':6, 'AUTO':7, 'RTL':8, 'SMARTRTL':9, 'GUIDED':10}
#     systemStates = {'UNINIT':0, 'BOOT':1, 'CALIBRATING':2, 'STANDBY':3, 'ACTIVE':4, 'CRITICAL':5, 'EMERGENCY':6, 'POWEROFF':7}
#     global state
#     print('Start of saving measurements in log file')
#     Events.info('Start of saving measurements in log file')	
#     headers = 'eph' + \
#             ';' + 'epv' + \
#             ';' + 'fix_type' + \
#             ';' + 'satellites'  + \
#             ';' + 'gps_status' + \
#             ';' + 'ekf' + \
#             ';' + 'latitude' + \
#             ';' + 'longitude' + \
#             ';' + 'altitude' + \
#             ';' + 'north' + \
#             ';' + 'east' + \
#             ';' + 'down' + \
#             ';' + 'pitch' + \
#             ';' + 'yaw' + \
#             ';' + 'roll' + \
#             ';' + 'Vx' + \
#             ';' + 'Vy' + \
#             ';' + 'Vz' + \
#             ';' + 'groundspeed' + \
#             ';' + 'voltage' + \
#             ';' + 'current' + \
#             ';' + 'power' + \
#             ';' + 'last_heartbeat' + \
#             ';' + 'armed' + \
#             ';' + 'mode' + \
#             ';' + 'armable' + \
#             ';' + 'system_status'
#     Events.info(headers)
#     while p.state > 1 :
#         mode = modeStates.get(vehicle.mode.name)
#         sys_status = systemStates.get(vehicle.system_status.state)
#         info = str(vehicle.gps_0.eph) + \
# 			';' + str(vehicle.gps_0.epv) + \
# 			';' + str(vehicle.gps_0.fix_type) + \
# 			';' + str(vehicle.gps_0.satellites_visible) + \
#         	';' + str(vehicle.gps_0) + \
# 			';' + str(int(vehicle.ekf_ok)) + \
# 			';' + str(vehicle.location.global_frame.lat) + \
# 			';' + str(vehicle.location.global_frame.lon) + \
# 			';' + str(vehicle.location.global_frame.alt) + \
# 			';' + str(vehicle.location.local_frame.north) + \
# 			';' + str(vehicle.location.local_frame.east) + \
# 			';' + str(vehicle.location.local_frame.down) + \
#             ';' + str(vehicle.attitude.pitch) + \
# 			';' + str(vehicle.attitude.yaw) + \
# 			';' + str(vehicle.attitude.roll) + \
# 			';' + str(vehicle.velocity[0]) + \
# 			';' + str(vehicle.velocity[1]) + \
# 			';' + str(vehicle.velocity[2]) + \
# 			';' + str(vehicle.groundspeed) + \
# 			';' + str(vehicle.battery.voltage) + \
# 			';' + str(vehicle.battery.current) + \
#         	';' + str(vehicle.battery.level) + \
# 			';' + str(vehicle.last_heartbeat) + \
# 			';' + str(int(vehicle.armed)) + \
# 			';' + str(int(vehicle.is_armable)) + \
# 			';' + str(mode) + \
# 			';' + str(sys_status) 
#         info = ((info.replace('None', '-1')).replace('GPSInfo:fix=', '')).replace('num_sat=', '') 
#         Values.info(info)
#         time.sleep(1/p.sensorFrequency)


# def StopFromQgc(vehicle) : 
# 	# This function allows to stop the autonomous mode when we get a text from QGC 
# 	#       connexion_string - link to listen communication 
# 	global state 	
# 	Events.info('Starting listening to Qgc')


# 	while True : 
# 		msg = vehicle.recv_match(type='COMMAND_ACK', blocking=True)
# 		print(msg)
 			

# 	# Method for when we receive the text
# 	def my_method(self, name, msg):
# 		global state 
# 		if  msg.command == 203 or vehicle.mode.name == "GUIDED": 	
# 			print("Command received from the Gound station, switching mode ...")
# 			Events.info('Command received from the Gound station, switching mode')
# 			vehicle.mode = dronekit.VehicleMode("GUIDED")
# 			p.state = 2

# 	# Listener 
# 	vehicle.add_message_listener('COMMAND_ACK',my_method)
# 	while p.state == 3 :	
# 		time.sleep(1)
# 	vehicle.remove_message_listener('COMMAND_ACK',my_method)


