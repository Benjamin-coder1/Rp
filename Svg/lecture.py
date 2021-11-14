
import pickle, cv2, sys
import numpy as np

speed = 58
frequency = 0
fileColor = open( "color.p" ,"rb")
fileResult = open( "result.p" ,"rb")

while True : 
    try : 
        color = pickle.load(fileColor)
        result = pickle.load(fileResult)
    except EOFError: break

    # resize data 
    expected = 300
    height, width = color.shape[:2]        
    aspect = width / height
    resized_image = cv2.resize(color, (round(expected * aspect), expected))
    crop_start = round(expected * (aspect - 1) / 2)
    color = resized_image[0:expected, crop_start:crop_start+expected]

    # display data 
    for res in result : 
        xmin,ymin,xmax,ymax,milx, mily, x, y, z, frequency = res
        pos = str(round(x,2))+ ' ' + str(round(y,2)) + ' ' + str(round(z,2))
        cv2.circle(color, ( milx , mily ), 3, (255,0,0), -1)
        cv2.rectangle(color, (xmin, ymin), (xmax, ymax), (0, 0, 0), 2)
        cv2.putText(color, pos, (xmin - 30, ymin - 10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0) )
    
    if len(result) != 0 : 
        cv2.putText(color, str( frequency ) + "Hz", (250,290), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0) )
        cv2.putText(color, str(len(result)) + " obj" , (250,270), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0) )

        

    cv2.imshow("Image",  color)
    cv2.waitKey(speed)
