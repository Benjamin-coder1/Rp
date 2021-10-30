import pickle, cv2, time
import Parameters as p

speed = 58
frequency = 0
fileColor = open( "svg/color.p" ,"rb")
timeLst = []

## Configuration of the CNN
net = cv2.dnn.readNetFromCaffe(p.configFile, p.weightFile)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)    
classNames = ("background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair",
            "cow", "diningtable", "dog", "horse",
            "motorbike", "person", "pottedplant",
            "sheep", "sofa", "train", "tvmonitor")   
inScaleFactor, meanVal , expected = [0.007843 , 127.53,  300]  # paraeters for CNN

while True : 
    try : 
        color = pickle.load(fileColor)
    except EOFError: break

    deb = time.time()

    # Image processing  
    height, width = color.shape[:2]        
    aspect = width / height
    resized_image = cv2.resize(color, (round(expected * aspect), expected))
    crop_start = round(expected * (aspect - 1) / 2)
    crop_img = resized_image[0:expected, crop_start:crop_start+expected]
    blob = cv2.dnn.blobFromImage(crop_img, inScaleFactor, (expected, expected), meanVal, False)
    net.setInput(blob, "data")
    detections = net.forward("detection_out")

    timeLst.append(time.time() - deb )
    print( time.time() - deb )


import numpy as np
print("Moyenne : " + str(np.mean(timeLst)))
