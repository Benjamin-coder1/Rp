from Simu import * 

# This module is used to launch the simulator, it simulate a car mooving and turning in a field
# The attribute used to control the car are the following 
#       rec.angle - set the steering angle of the car
#       rec.speed  - set the speed of the car 
#       rec.on -    set True to start vehicle / False to stop it 
# The attribute used to see what the car can see is 
#       rec.pc - give the point cloud seen by the camera in top view (2D)
pcInitial = initializePC(l0 = 3)
rec = rectangle(pcInitial, (5.5,2), L=3.5, l=1.5)

# Main loop in which you should write your code using the previous described attribute of the vehicle 
while True : 
    #********#    START CODING HERE   #******#






    #********#    STOP CODING HERE   #******#
    fig.canvas.draw_idle()
    plt.pause(sleepingTime)

        
 