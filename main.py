import numpy as np
import time
import cv2

from functions_cvplt import *
from cvplt import *

class Main:
    def __init__(self):
        # Get Time
        self.timeTotalStartDouble = time.time()
        self.timeTotalElapsedDouble = time.time() - self.timeTotalStartDouble
        print("Main.__init__() timeTotalStart: {}".format(self.timeTotalStartDouble))
        # Fundamentals
        self.exitBool = False
        self.loopCounterInt = 0
        # User Parameters
        self.renderResTuple = (800,800)
        self.dispResTuple = (1600,1600)
        # Inferred Parameters
        self.renderCenterTuple = Functions.get_screencenter(self.renderResTuple)
        # Create Render & Display Arrays
        self.renderArray = Functions.get_screenarray_colour(self.renderResTuple, [80,80,80])
        self.dispArray = Functions.get_screenarray_colour(self.dispResTuple, [80,80,80])
    
    def loop(self, loopCounterInt, timeTotalElapsedDouble):
        # Get Time
        timeTotalElapsedDouble = time.time() - self.timeTotalStartDouble
        print("Main.loop() loop#: {}, timeElapsed: {}".format(loopCounterInt, timeTotalElapsedDouble))
        # Do Loop
        data_demo_0 = np.array([10,20,30,np.nan,25,25,np.nan,1,1,2,3,4,5,np.nan,15,15,np.nan,15,np.nan,15,np.nan,15])
        self.renderArray = cvplt.draw_plot("Demo Plot 0", data_demo_0, self.renderArray, [400,25], [300,50], [1,1,1], [200,200,200], [150,150,150])
        data_demo_1 = (np.random.rand(240)*100)-50
        self.renderArray = cvplt.draw_plot("Demo Plot 1", data_demo_1, self.renderArray, [100,25], [200,50], [1,1,1], [200,200,200], [50,50,200])
        data_demo_2 = np.array((50,20,20,20,80,80,80,80,80,80,20,20,20))
        self.renderArray = cvplt.draw_plot("Demo Plot 2", data_demo_2, self.renderArray, [250,250], [400,400], [50,50,50], [200,200,200], [140,240,140])
        data_demo_3 = (np.random.rand(300)*10000)-5000
        self.renderArray = cvplt.draw_plot("Demo Plot 3", data_demo_3, self.renderArray, [400,550], [600,240], [220,220,220], [1,1,1], [20,20,200])
        data_demo_4 = (np.random.rand(550)*10000)-5000
        self.renderArray = cvplt.draw_plot("Demo Plot 4", data_demo_4, self.renderArray, [200,750], [600,100], [1,1,1], [200,200,200], [200,20,200])
        # Draw Loop
        self.draw()
        # End Loop
        loopCounterInt += 1
        return loopCounterInt, timeTotalElapsedDouble

    def draw(self):
        self.dispArray = cv2.resize(self.renderArray, self.dispResTuple)
        cv2.imshow("dispArray", self.dispArray)
        cv2.waitKey(1)
        return 

if __name__ == "__main__":
    # Main Init
    print("----- Main Init -----")
    main = Main()
    # Main Loop
    print("--- Main Loop ---")
    #while (main.exitBool == False) and (main.timeTotalElapsedDouble <= 1):
    main.loopCounterInt, main.timeTotalElapsedDouble = main.loop(main.loopCounterInt, main.timeTotalElapsedDouble)
    # End
    print("--- Main End ---")
    time.sleep(100)