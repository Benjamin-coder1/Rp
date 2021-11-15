import sys, time, threading  
sys.path.append("../ObstacleDetection")
sys.path.append("..")
import ConfigParameters as p
import ObjectDetection, Tools, MyVehicle



###################################################################################
#####							START MACHINE 								#######
###################################################################################

p.EventLogger.info('Launch of the Program - %s', time.strftime('%d/%m/%Y'))


while p.state != 0 : 	

	####################################################################################

	# Display mode 
	if p.state == 1 : 
		Tools.disp('\n## ---- Initialisation of the vehicle ---- ##', 3, p.EventLogger)

	while p.state == 1 :
		##############################
		# -- Initialisation state -- #
		##############################		

		# Create an instance of vehicle 
		vehicle = MyVehicle.MyVehicle(p.connection_string, p.EventLogger)
		vehicle.InitialisationVehicle()
		p.EventLogger.propagate, p.MeasureLogger.propagate = False , False	
	
		# Changing state 
		p.state = 2

		# start saving values of the vehicle 
		# threadValue = threading.Thread(target=setValue, args=[vehicle])
		# threadValue.start()	


	####################################################################################

	# Display mode 
	if p.state == 2 : 
		Tools.disp('## ---- Groud station control ---- ##' , 3, p.EventLogger)
	

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
		Tools.disp('## ---- Autonomous mode ---- ##', 3, p.EventLogger)
	
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
Tools.disp('## ---- Vehicle OFF ---- ##', 2, p.EventLogger)
