############################
## ------ Main ------ ##
############################

import sys, time, threading  
sys.path.append("../..")
import ConfigParameters as p
from Initialisation import *
sys.path.append("../ObstacleDetection")
from ObjectDetection import detect_obstacle

# This script implements the state machine of the vehicle. It is automatically launch at the activation 
Events.info('Launch of the Program - %s', time.strftime('%d/%m/%Y'))


while p.state != 0 : 	

	####################################################################################

	# Display mode 
	if p.state == 1 : 
		print('\033[94m' + '\n## ---- Initialisation of the vehicle ---- ##' + '\033[0;0m')
		Events.info('Initialisation of the vehicle')

	while p.state == 1 :
		##############################
		# -- Initialisation state -- #
		##############################		

		# Connexion with the vehicle
		vehicle = getConnexionVehicle(p.connection_string, Events)	
		Events.propagate, Values.propagate = False , False	
	
		# Initialization of the Vehicle
		vehicle = InitialisationVehicle(vehicle, Events)		
		
		# Changing state 
		p.state = 2

		# start saving values of the vehicle 
		# threadValue = threading.Thread(target=setValue, args=[vehicle])
		# threadValue.start()	


	####################################################################################

	# Display mode 
	if p.state == 2 : 
		print('\033[94m' + '## ---- Groud station control ---- ##' + '\033[0;0m')
		Events.info('Groud station control')

	while p.state == 2 : 
		###############################
		# -- Groud station control -- #
		###############################
		
		# Switching mode
		msg = vehicle.recv_match(type = 'HEARTBEAT', blocking = True)
		if msg:
			mode = mavutil.mode_string_v10(msg)
			if mode == "MANUAL" :
    				p.state = 3 


		# Time of sleeping 
		time.sleep(p.sleepTime)

	####################################################################################

	# Display mode 
	if p.state == 3 : 
		print('\033[94m' + '## ---- Autonomous mode ---- ##' + '\033[0;0m')
		Events.info('Autonomous mode')

	# Start Listening what is comming from the ground station
	# threadStopFromQgc =  threading.Thread(target=StopFromQgc, args=[vehicle])
	# threadStopFromQgc.start()	

	while p.state == 3 :
		###############################
		# --   Autonomous control  -- #
		###############################
		
		# Set speed
		setSpeed(vehicle, 1e-1)

		# Time of sleeping	
		time.sleep(p.sleepTime)

	# Stop listening what is comming from ground station 
	# threadStopFromQgc.join()
	vehicle.groundspeed = 0

	####################################################################################

# End of the programe 
# threadValue.join()
vehicle.close()
Events.info('Vehicle off')
