import logging,os, sys
import Tools  
PATH = os.getcwd().split('/rp')[0] + '/rp' 

state = 1   # this variable represent the curent state of the machine : 
				# state = 0 --> machine off
				# state = 1 --> Initialisation 
				# state = 2 --> manual control 
				# state = 3 --> autonomous mode 

# sleep time between two loops 
sleepTime = 1  

# informations about the log file 
logFileEvent = {}
logFileEvent['name'] = PATH +  "/LogFile/Events.csv"   
logFileEvent['format'] = '%(asctime)s;%(levelname)s;%(message)s'
logFileEvent['dateFormat'] = '%H:%M:%S'
logFileEvent['level'] = logging.INFO
EventLogger = Tools.CreateLogger(logFileEvent)

logFileMeasure = {}
logFileMeasure['name'] = PATH + "/LogFile/Values.csv"   
logFileMeasure['format'] = '%(asctime)s:%(msecs)03d;%(message)s'
logFileMeasure['dateFormat'] = '%H:%M:%S'
logFileMeasure['level'] = logging.INFO
MeasureLogger = Tools.CreateLogger(logFileMeasure)

# frequency of saving sensor data (Hz)
sensorFrequency = 10

# Connexion string by default 
connection_string = '/dev/ttyUSB0'   # '/dev/ttyUSB0'

# Obstacle detection parameters
Nbcsvtmax = 5   # number of consecutive frames for stopping
conf = 0.2   # percentage for object detection  
stop = False   # Stop the vehicle or not 
distMin = 0.3		# Min distance before an obstacle (m)
configFile = PATH + "/Fonctionality/ObstacleDetection/CaffeeModel/SSD_MobileNet.prototxt"    # config of model
weightFile = PATH + "/Fonctionality/ObstacleDetection/CaffeeModel/SSD_MobileNet.caffemodel"  # weight of model 

# Saving camera
fileNameColor = PATH + "/Svg/color.p"
fileNamePointCloud = PATH + "/Svg/pointCloud.p"
fileNameResult = PATH + "/Svg/result.p"


