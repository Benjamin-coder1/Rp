from  pymavlink  import mavutil
import sys 
sys.path.append("..")
import Tools

class MyVehicle : 

    def __init__(self, connection_string, EventLogger) :
        self.EventLogger = EventLogger
        self.vehicle = self.getConnexionVehicle(connection_string) 
    
    def getConnexionVehicle(self, connection_string) : 
        """This function establishes the connexion with the true vehicle
        	connection_string - identification of the connexion between the computer and the vehicle """
        
        Tools.disp("Connecting to vehicle on : %s" % (connection_string,), 4 , self.EventLogger ) 
        while True : 
            try : 
                Tools.disp('>> CONNEXION VEHICLE ... ', 2, self.EventLogger)
                vehicle = mavutil.mavlink_connection(connection_string,  baud=57600)
                vehicle.wait_heartbeat()
                Tools.disp('CONNECTED TO THE VEHICLE', 1, self.EventLogger)
                self.EventLogger.propagate = False
                return vehicle
            except : 
                Tools.disp('Connextion failed', 0, self.EventLogger)                
                connection_string = str(input('Connecting port : '))
    
    def InitialisationVehicle(self) : 
        """This function allows to initialize the vehicle  """

        ## 1- SET THE MODE
        Tools.disp('>> Setting MANUAL Mode ... ', 2, self.EventLogger)        
        self.vehicle.mav.set_mode_send(self.vehicle.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,0)
        while True:
            ack_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()
            # Check if command in the same in `set_mode`
            if ack_msg['command'] != mavutil.mavlink.MAVLINK_MSG_ID_SET_MODE:
                continue
            # Print the ACK result !
            print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
            break
        Tools.disp('MANUAL mode activated', 1, self.EventLogger)  
         
        ## 2 - ARMING 
        Tools.disp('>> Arming the vehicle ... ', 2, self.EventLogger)   
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system,
            self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0)
        self.vehicle.motors_armed_wait()
        Tools.disp('Vehicle armed.', 1, self.EventLogger)  

    def setSpeedPin(self, pin) : 
        """ This function define which pin to use to control speed """
        self.SpeedSpin = pin 
        Tools.disp('Speed pin set on %d' % (pin,), 4 , self.EventLogger)

    def setOrientationPin(self, pin) : 
        """ This function define which pin to use to control speed """
        self.OrientationPin = pin     
        Tools.disp('Orientation pin set on %d' % (pin,), 4 , self.EventLogger)

    def Go(self, speed) : 
        """This function set a speed of the bottom wheels"""
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system, self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,            # first transmission of this command
            self.SpeedSpin + 8,  # servo instance, offset by 8 MAIN outputs
            2e4*speed, # PWM pulse-width
            0,0,0,0,0     # unused parameters
        )
    
    def Turn(self, angle) : 
        """This function set a speed of the bottom wheels"""
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system, self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,            # first transmission of this command
            self.OrientationPin + 8,  # servo instance, offset by 8 MAIN outputs
            2e4*angle, # PWM pulse-width
            0,0,0,0,0     # unused parameters
        )