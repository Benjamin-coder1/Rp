import cv2, time, threading                      
import numpy as np                       
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import Parameters as p 
from Initialisation import *
import pickle


pipe, align, cfg = [rs.pipeline() , rs.align(rs.stream.color), rs.config()]

print('Connexion realsense Camera ... ')
Events.info("Connexion realsense Camera")
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipe.start(cfg)
cleanFrames()
print('\033[92m' + 'Camera configurated and connected.' + '\033[0m')  
Events.info("Camera configurated and connected")   
done = True

