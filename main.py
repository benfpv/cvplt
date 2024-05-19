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
        self.renderResTuple = (800,400)
        self.dispResTuple = (800,400)
        # Inferred Parameters
        self.renderCenterTuple = Functions.get_screencenter(self.renderResTuple)
        # Create Render & Display Arrays
        self.renderArray = Functions.get_screenarray_colour(self.renderResTuple, [80,80,80])
        self.dispArray = Functions.get_screenarray_colour(self.dispResTuple, [80,80,80])
    
    def loop(self, loopCounterInt, timeTotalElapsedDouble):
    # (renderArray, data, plotBeginXY, plotEndXY, plotTitle="", plotBackgroundColour=[0,0,0], plotOutlineColour=[250,250,250], plotValuesColour=[250,250,250])
        # Get Time
        timeTotalElapsedDouble = time.time() - self.timeTotalStartDouble
        print("Main.loop() loop#: {}, timeElapsed: {}".format(loopCounterInt, timeTotalElapsedDouble))
        # Do Loop
        data_demo_0 = np.array([10,20,30,np.nan,25,25,np.nan,1,1,2,3,4,5,np.nan,15,15,np.nan,15,np.nan,15,np.nan,15])
        self.renderArray = cvplt.draw_plot(self.renderArray, data_demo_0, [0,0], [400,50])
        data_demo_1 = (np.random.rand(240)*100)-50
        data_demo_1[40:80] = np.nan
        data_demo_1[120:180] = np.nan
        self.renderArray = cvplt.draw_plot(self.renderArray, data_demo_1, [80,60], [300,120], "Demo Plot 1", [60,60,60], [150,200,250], [70,160,160])
        data_demo_2 = np.array((50,20,20,20,80,80,80,80,80,80,20,20,20))
        self.renderArray = cvplt.draw_plot(self.renderArray, data_demo_2, [200,110], [700,260], "Demo Plot 2", [1,1,1], [10,10,250], [250,250,250])
        data_demo_3 = (np.random.rand(300)*10000)-5000
        data_demo_3[200::] = np.nan
        self.renderArray = cvplt.draw_plot(self.renderArray, data_demo_3, [460,220], [640,350], "Demo Plot 3", [160,160,50], [250,250,250], [250,250,100])
        data_demo_4 = (np.random.rand(550)*10000)-5000
        self.renderArray = cvplt.draw_plot(self.renderArray, data_demo_4, [0,320], [650,380], "Demo Plot 4", [200,200,200], [10,10,10], [180,180,60])
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