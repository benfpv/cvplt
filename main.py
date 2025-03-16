import numpy as np
import time
import cv2

from cvplt import *

class Main:
    def __init__(self):
        # User Parameters
        self.renderResTuple = (640,480)
        self.dispResTuple = (640,480)
        # Auto-Inferred Parameters
        self.renderCenterTuple = cvplt.get_screencenter(self.renderResTuple)
        # Create Render & Display Arrays
        self.backgroundColour = [80,80,80] # E.g., 80, [80, 80, 80]
        self.renderArray = cvplt.get_screenarray_colour(self.renderResTuple, self.backgroundColour)
        self.dispArray = cvplt.get_screenarray_colour(self.dispResTuple, self.backgroundColour)
        
    def loop(self):
        ### Data ### 
        # This section is where data updates would be handled - all are static for this demo, since demo is only 1 loop.
        data_demo_0 = np.array([10,20,30,np.nan,25,25,np.nan,1,1,2,3,4,5,np.nan,15,15,np.nan,15,np.nan,15,np.nan,15])
        data_demo_1 = (np.random.rand(240)*100)-50
        data_demo_1[40:80] = np.nan
        data_demo_1[120:180] = np.nan
        data_demo_2 = np.array((50,20,20,20,80,80,80,80,80,80,20,20,20))
        data_demo_3 = (np.random.rand(300)*10000)-5000
        data_demo_3[200::] = np.nan
        data_demo_4 = (np.random.rand(550)*10000)-5000
        data_demo_5 = np.array([5.5])
        data_demo_coords = np.array([[-1,-5],[-20,-2],[0,0],[0,5],[10,10],[10,0]], dtype="int")
        ### Do Loop ###
        # This is where data is fed into cvplt functions to plot onto the render array.
        t_0 = time.time()
        self.renderArray = cvplt.draw_plot(data_demo_0)
        t_1 = time.time()
        print("data_demo_0: {}".format(t_1 - t_0))
        t_1 = time.time()
        self.renderArray = cvplt.draw_plot(data_demo_1, self.renderArray, plotBeginXY=[80,60], plotEndXY=[300,120], plotTitle="Demo Plot 1", plotBackgroundColour=[60,60,60], plotOutlineColour=[150,200,250], plotValuesColour=[70,160,160])
        t_2 = time.time()
        print("data_demo_1: {}".format(t_2 - t_1))
        t_2 = time.time()
        self.renderArray = cvplt.draw_plot(data_demo_2, renderArray=self.renderArray, plotBeginXY=[200,110], plotEndXY=[500,260], plotTitle="Demo Plot 2", plotBackgroundColour=[1,1,1], plotOutlineColour=[10,10,250], plotValuesColour=[250,250,250])
        t_3 = time.time()
        print("data_demo_2: {}".format(t_3 - t_2))
        t_3 = time.time()
        self.renderArray = cvplt.draw_plot(data_demo_3, renderArray=self.renderArray, plotBeginXY=[460,220], plotEndXY=[630,350], plotTitle="Demo Plot 3", plotBackgroundColour=[160,160,50], plotOutlineColour=[250,250,250], plotValuesColour=[250,250,100])
        t_4 = time.time()
        print("data_demo_3: {}".format(t_4 - t_3))
        t_4 = time.time()
        self.renderArray = cvplt.draw_plot(data_demo_4, renderArray=self.renderArray, plotBeginXY=[0,320], plotEndXY=[600,380], plotTitle="Demo Plot 4", plotBackgroundColour=[200,200,200], plotOutlineColour=[10,10,10], plotValuesColour=[180,180,60])
        t_5 = time.time()
        print("data_demo_4: {}".format(t_5 - t_4))
        t_5 = time.time()
        self.renderArray = cvplt.draw_plot(data_demo_5, renderArray=self.renderArray, plotBeginXY=[200,0], plotEndXY=[280,50], plotTitle="Demo Plot 5", plotBackgroundColour=[120,60,120], plotOutlineColour=[30,30,90], plotValuesColour=[240,200,200])
        t_6 = time.time()
        print("data_demo_5: {}".format(t_6 - t_5))
        # Do Coords Plotting
        t_6 = time.time()
        self.renderArray = cvplt.draw_plot_coords(data_demo_coords, self.renderArray, plotBeginXY=[200,200], plotEndXY=[380,280], plotTitle="Demo Plot Coords", plotBackgroundColour=[200,200,200], plotOutlineColour=[10,10,10], plotValuesColour=[10,100,60])
        t_7 = time.time()
        print("data_demo_coords: {}".format(t_7 - t_6))
        # Do Neurons Plotting
        t_7 = time.time()
        
        t_8 = time.time()
        print("data_demo_neurons: {}".format(t_8 - t_7))
        # Draw Loop
        self.draw()
        return
    
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
    main.loop()
    # End
    print("--- Main End ---")
    end_sleep_duration = 30
    for i in range(end_sleep_duration):
        print("\rPaused for {} /{} Seconds. Press 'Ctrl+C' in Command Prompt to Unpause & Exit.".format(i, end_sleep_duration), end="", flush=True)
        time.sleep(1)
    time.sleep(30)