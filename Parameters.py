import logging 


state = 1   # this variable represent the curent state of the machine : 
				# state = 0 --> machine off
				# state = 1 --> Initialisation 
				# state = 2 --> manual control 
				# state = 3 --> autonomous mode 

# sleep time between two loops 
sleepTime = 1  

# name of the CSV file for parameters by default
vehicleParameters = "vehicleParameters.csv"  

# informations about the log file 
logFileEvent = {}
logFileEvent['name'] = "logFile/Events.csv"   
logFileEvent['format'] = '%(asctime)s;%(levelname)s;%(message)s'
logFileEvent['dateFormat'] = '%H:%M:%S'
logFileEvent['level'] = logging.INFO

logFileValue = {}
logFileValue['name'] = "logFile/Values.csv"   
logFileValue['format'] = '%(asctime)s:%(msecs)03d;%(message)s'
logFileValue['dateFormat'] = '%H:%M:%S'
logFileValue['level'] = logging.INFO


# frequency of saving sensor data (Hz)
sensorFrequency = 10

# Connexion string by default 
connection_string = '/dev/ttyUSB0'   # '/dev/ttyUSB0'

# Obstacle detection parameters
Nbcsvtmax = 5   # number of consecutive frames for stopping
conf = 0.2   # percentage for object detection  
stop = False   # Stop the vehicle or not 
distMin = 0.3		# Min distance before an obstacle 
configFile = "./CaffeeModel/SSD_MobileNet.prototxt"    # config of model
weightFile = "./CaffeeModel/SSD_MobileNet.caffemodel"  # weight of model 

# Saving camera
fileNameColor = "svg/color.p"
fileNamePointCloud = "svg/pointCloud.p"
fileNameResult = "svg/result.p"


