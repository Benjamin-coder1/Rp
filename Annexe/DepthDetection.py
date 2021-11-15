
import cv2, sys, time
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import numpy as np
import matplotlib.pyplot as plt 


done = False 
pipe, align, cfg = [rs.pipeline() , rs.align(rs.stream.color), rs.config()]
while not done : 
    try:
        print('Connexion realsense Camera ... ')
        cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipe.start(cfg)
        print('\033[92m' + 'Camera configurated and connected.' + '\033[0m')  
        done = True
    except Exception as e:
        print('\033[91m' + str(e.args) + '\033[0m') 
        for tm in range(30) : 
            sys.stdout.write("\r{0}".format(" "*20))
            sys.stdout.write("\r{0}".format("Reconnection attempt in " + str(30 - tm) + " s ...", 10))
            sys.stdout.flush()
            time.sleep(1)


while True : 
    frameset = pipe.wait_for_frames()
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data())
    depth_grad = np.abs( np.gradient(depth )[0] ) + np.abs( np.gradient(depth )[1] )
    depth_grad =  ( depth_grad - np.min(depth_grad) ) / (np.max(depth_grad) - np.min(depth_grad) )

    depth_grad =  (depth_grad > 0.1) 

    cv2.imshow('image', depth_grad)
    cv2.waitKey(1)
