import matplotlib.pyplot as plt 
import numpy as np
import time, cv2, threading, cmath, keyboard

sleepingTime = 1e-2
fig, ax = plt.subplots()
ax.grid(True)
plt.xlim(2.5,22.5)
plt.ylim(-10,10)

##############################################
###########     DEFINE SHAPES      ###########     
##############################################

class rectangle() :
    def __init__(self, pcGlob, center, L, l) : 
        self.L = L   # Longueur
        self.l = l   # Largeur 
        self.angle = np.pi/6    # Angle roue avant         
        self.speed =  5e-1           # Loop
        self.on = True     # vehicle on 
        self.pcGlob = pcGlob    # Point cloud environement 
        self.vertices = cv2.boxPoints(( center , (self.l, self.L), 0)) 
        threading.Thread( target=self.dispXY ).start()
        threading.Thread( target=self.moove ).start()
        threading.Thread( target=self.attachCircle ).start()
        threading.Thread( target=self.detectColision ).start()
        threading.Thread( target=self.dispText ).start()
        threading.Thread( target=self.visionFieldFace ).start()
        threading.Thread( target=self.manualControl ).start()
        
    def manualControl(self): 
        print(('Manual Control : OK'))
        while True :
            if keyboard.read_key() == "right" : 
                self.angle += 1e-2
            elif keyboard.read_key() == "left" : 
                self.angle -= 1e-2
            elif keyboard.read_key() == "up" : 
                self.speed = min( 5, self.speed + 5e-1)              
            elif keyboard.read_key() == "down" : 
                self.speed = max( 1e-1, self.speed - 5e-1)  
            if self.speed == 1e-1 : 
                self.on = False
                continue
            self.on = True
            time.sleep(sleepingTime)
            
    def attachCircle(self) : 
        print(('Display rotation circle : OK'))
        ### DEFINE CIRCLE
        circInt = circle(self.L/np.tan(self.angle), self.C)
        circExt = circle(np.sqrt( self.L**2 + (self.l + self.L/np.tan(self.angle))**2 ), self.C)
        while True : 
            circInt.centre = self.C
            circExt.centre = self.C
            circInt.rayon = self.L/np.tan(self.angle)
            circExt.rayon = np.sqrt( self.L**2 + (self.l + self.L/np.tan(self.angle))**2 )
            time.sleep(sleepingTime)


    def moove(self) :
        print(('Mooving : OK'))         
        while True :      
            self.deltaAngle = np.sin(self.angle)*5e-2/self.L     # angle of mooving at constant speed at eah loop 
            M = np.array([[np.cos(self.deltaAngle), np.sin(self.deltaAngle)],[-np.sin(self.deltaAngle), np.cos(self.deltaAngle)]])
            x0, y0 = self.vertices[1,:]
            x1, y1 = self.vertices[2,:]
            eps = (x1 - x0)/abs(x1 - x0)
            if x1 != x0 :             
                r =  (y1 - y0)/(x1 - x0) 
                x = x1 + eps*self.L / (np.tan(self.angle) * np.sqrt( 1 + r**2 ) )
                y = y1 + eps*r*self.L / (np.tan(self.angle) * np.sqrt( 1 + r**2 ) ) 
            else : 
                y = y0  - (self.l + self.L/np.tan(self.angle) )  

            self.C = np.array([[x],[y]])     
            if not self.on : 
                time.sleep(1e-2)
                continue    
            for i in range(4) : 
                X = np.dot(M, np.reshape( self.vertices[i,:], (-1,1) ) - self.C ) + self.C
                self.vertices[i,0], self.vertices[i,1] = X[0], X[1]

            time.sleep(1e-1/self.speed)
        
    def detectColision(self) :     
        print(('Detection colision : OK'))    
        self.touched = False
        while True : 
            x0, y0 = self.vertices[0,:]
            x1, y1 = self.vertices[1,:]
            x2, y2 = self.vertices[2,:]
            x3, y3 = self.vertices[3,:]

            ah = (y0 - y1) / (x0 - x1)
            bh1 = y0 - ah*x0
            bh2 = y3 - ah*x3

            av = (y2 - y1) / (x2 - x1)
            bv1 = y3 - av*x3
            bv2 = y2 - av*x2

            xtouched, ytouched = [], []
        
            if ah > 0 and bh1 > bh2: 
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y > ah*x + bh2 and y < ah*x + bh1 and y < av*x + bv1 and y > av*x + bv2 : 
                        xtouched.append(x)
                        ytouched.append(y)
            elif ah < 0 and bh1 > bh2 : 
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y > ah*x + bh2 and y < ah*x + bh1 and y > av*x + bv1 and y < av*x + bv2 : 
                        xtouched.append(x)
                        ytouched.append(y)
            elif ah > 0 and bh1 < bh2 : 
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y < ah*x + bh2 and y > ah*x + bh1 and y > av*x + bv1 and y < av*x + bv2 : 
                        xtouched.append(x)
                        ytouched.append(y)
            elif ah < 0 and bh1 < bh2 : 
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y < ah*x + bh2 and y > ah*x + bh1 and y < av*x + bv1 and y > av*x + bv2 : 
                        xtouched.append(x)
                        ytouched.append(y)

            if np.size(xtouched) != 0 : 
                self.figPlot.set_color('red')
                self.touched = True
            else :  self.figPlot.set_color('green')

            time.sleep(sleepingTime)

    def visionFieldFace(self) :
        print(('Field of vision : OK')) 
        visionScatter = ax.scatter([],[], color='k')
        self.fieldFace = 86*np.pi/180
        t = np.linspace(0,10, 100)
        fieldplot1 = ax.plot([],[], color='blue')[0]
        fieldplot2 = ax.plot([],[], color='blue')[0]
        alpha = (np.pi - self.fieldFace) / 2
        M1 = np.array([[np.cos(alpha), -np.sin(alpha)],[np.sin(alpha), np.cos(alpha)]])
        M2 = np.array([[np.cos(self.fieldFace), -np.sin(self.fieldFace)],[np.sin(self.fieldFace), np.cos(self.fieldFace)]])
        l1 = 0.1  # for random
        while True : 
        
            x0, y0 = self.vertices[0,:]
            x1, y1 = self.vertices[1,:]
            x3, y3 = self.vertices[3,:]
            xc , yc = (x0 + x3)/2, (y0 + y3)/2

            r = (y3 - y0) / (x3 - x0)
            eps = (x3 - x0) / abs(x3 - x0)
            u = np.array([[1], [r]])*eps/np.sqrt(1 + r**2)

            # Droite num 1
            v = np.dot(M1,u)
            x = v[0]*t + xc
            y = v[1]*t + yc
            a1, b1 = v[1]/v[0] , yc - v[1]/v[0]*xc            
            fieldplot1.set_xdata(x)
            fieldplot1.set_ydata(y)            

            # Droite num 2 
            v = np.dot(M2, np.dot(M1,u) )
            x = v[0]*t + xc
            y = v[1]*t + yc
            a2, b2 = v[1]/v[0] , yc - v[1]/v[0]*xc
            fieldplot2.set_xdata(x)
            fieldplot2.set_ydata(y)

            # Droite num 3
            a3 = (y0 - y3)/(x0 - x3) 
            b3 = y3 - x3*(y0 - y3)/(x0 - x3)

            # Detect points we should see
            xseen, yseen = [], []
            phase = cmath.phase(complex(x0 - x1, y0 - y1))
            if  phase > np.pi/2 :  
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y > a3*x+b3 and y > a2*x+b2 and x < (y - b1)/a1 : 
                        xseen.append(x + 2*l1*np.random.rand() - l1 )
                        yseen.append(y + 2*l1*np.random.rand() - l1 )
            
            elif phase < np.pi/2 and phase > 0:  
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y > a3*x+b3 and y > a1*x+b1 and x > (y - b2)/a2 : 
                        xseen.append(x + 2*l1*np.random.rand() - l1 )
                        yseen.append(y + 2*l1*np.random.rand() - l1 )
            
            elif phase > -np.pi/2 and phase < 0: 
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y < a3*x+b3 and y < a2*x+b2 and x > (y - b1)/a1 : 
                        xseen.append(x + 2*l1*np.random.rand() - l1 )
                        yseen.append(y + 2*l1*np.random.rand() - l1 )
            
            elif phase < -np.pi/2 :  
                for ind in range(np.size(self.pcGlob[0])) : 
                    x = self.pcGlob[0][ind]
                    y = self.pcGlob[1][ind]
                    if y < a3*x+b3 and y < a1*x+b1 and x < (y - b2)/a2  : 
                        xseen.append(x + 2*l1*np.random.rand() - l1 )
                        yseen.append(y + 2*l1*np.random.rand() - l1 )

            self.pc = [xseen, yseen]
            visionScatter.set_offsets(np.c_[xseen, yseen])
            time.sleep(sleepingTime)

    def dispText(self) :
        print(('Text interface : OK'))
        deb = time.time() 
        myText = ax.text(0.98, 0.88,"", transform=ax.transAxes, horizontalalignment='right', verticalalignment='center')
        while True : 
            infos = str(round(self.angle*180/np.pi,1)) + "°"            
            infos += "\n" + str( round(time.time() - deb)) + " s"
            infos += "\n" + str( round(self.speed,1) ) + " m/s"
            x0, y0 = self.vertices[0,:]
            x1, y1 = self.vertices[1,:]
            infos += "\n" + str( round(cmath.phase(complex(x0 - x1, y0 - y1)), 1) ) + " rad"
            if self.touched : infos +=  "\nTouched"
            else : infos += "\nGood"
            myText.set_text(infos)
            time.sleep(sleepingTime)

    def dispXY(self) : 
        print(('Display : OK'))
        self.figPlot = ax.plot([],[], color='g')[0]
        while True : 
            self.figPlot.set_xdata(list(self.vertices[:,0]) + [self.vertices[0,0]]) 
            self.figPlot.set_ydata(list(self.vertices[:,1]) + [self.vertices[0,1]]) 
            time.sleep(sleepingTime)

class circle() :
    def __init__(self, rayon, centre) :
        self.figPlot = ax.plot([],[], color='k', alpha=0.5, linestyle= 'dotted')[0] 
        self.rayon = rayon
        self.centre = centre
        threading.Thread( target=self.dispXY ).start()
    
    def dispXY(self) : 
        while True :           
            t = np.linspace(0,2*np.pi, 100)
            x = self.rayon*np.cos(t) + self.centre[0]
            y = self.rayon*np.sin(t) + self.centre[1]
            self.figPlot.set_xdata(x)
            self.figPlot.set_ydata(y)
            time.sleep(sleepingTime)
     
################################################
###########     INITIALISATION       ###########   
################################################


### DEFINE THE POINT CLOUD
def initializePC(l0) : 
    pcScatter = ax.scatter([],[], color='grey')  
    def getPointCloud() : 
        """ This function simulate a point cloud """
        ylim=[-6, 4]
        xini = 4
        x, y = [], []
        for nb in range(6) :
            row = np.array( [[xini + nb*l0,ylim[0]],[xini + nb*l0,ylim[1]]] ) 
            lineY = list(np.linspace(row[1,1], row[0,1], 100))
            y += lineY
            x += np.size(lineY)*[row[0,0]]
        return [x, y]
    pc = getPointCloud()
    pcScatter.set_offsets(np.c_[pc[0], pc[1]])
    return pc
 
  

