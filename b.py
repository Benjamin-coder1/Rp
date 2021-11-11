
import cv2, time, threading, pickle                   
import numpy as np                       
import pyrealsense2 as rs   
import matplotlib.pyplot as plt


# Point cloud computation
def getPointCloud(depth_frame) : 
    pc = rs.pointcloud()    
    points = pc.calculate(depth_frame)
    w = rs.video_frame(depth_frame).width
    h = rs.video_frame(depth_frame).height
    return np.asanyarray(points.get_vertices()).view(np.float32).reshape(h, w, 3)

def fittage(x,y) : 
    parametres = np.polyfit(x, y, 1) 
    angle = round(-np.arctan(parametres[0]) * 180/np.pi, 2)
    return parametres, angle   
    




print('Connexion realsense Camera ... ')
pipe, align, cfg = [rs.pipeline() , rs.align(rs.stream.color), rs.config()]
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipe.start(cfg)
print('Aligned')  


# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
x, y, z = [[], [],[]]

while True : 
    ## Connection to the Camera
    frameset = pipe.wait_for_frames()
    depth_frame = frameset.get_depth_frame()
    verts = getPointCloud(depth_frame)
    print(np.shape(verts))
    x, y = [[],[]]
    for i in range(480) : 
        for j in range(640) : 
            if np.prod(verts[i,j,:]) != 0 :
                if verts[i,j,0]< -0.05 and abs(verts[i,j,0]) < 0.5 and abs(verts[i,j,2]) < 0.5 and verts[i,j,1] < 0 :
                    x.append(verts[i,j,0])
                    y.append(verts[i,j,2])
                    z.append(-verts[i,j,1])
    
    plt.scatter(x,y, marker="x")
    # ax.scatter(x,y,z, marker='x' )

    # linear regression 
    deb = time.time()
    parametres, angle = fittage(x,y)
    print( time.time() - deb )
    
    # display
    abs = np.linspace(-0.225, -0.05,  100)
    ord = parametres[0]*abs+parametres[1]
    plt.plot(abs, ord, color='r')
    
    # compute angle 
    angle = round(-np.arctan(parametres[0]) * 180/np.pi, 2)
    print(angle)
    plt.show()

    



