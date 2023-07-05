import numpy as np

class Functions:
    def get_screensize(screenshot):
        #print("Functions.get_screensize()")
        if not screenshot.any():
            return []
        screenshape = screenshot.shape
        screensize = [screenshape[1], screenshape[0]]
        #print("- screensize: {}".format(screensize))
        return screensize
    
    def get_screendepth(screenshot):
        #print("Functions.get_screendepth()")
        if not screenshot.any():
            return []
        screendepth = len(screenshot.shape)
        #print("- screendepth: {}".format(screendepth))
        return screendepth

    def get_screencenter(screensize):
        #print("Functions.get_screencenter()")
        if not screensize:
            return []
        screencenter = (int(screensize[0]*0.5), int(screensize[1]*0.5))
        return screencenter

    def get_screenarray_colour(screensize, backgroundColour):
        #print("Functions.get_screenarray_colour()")
        if (not screensize) or (not backgroundColour):
            return []
        screenArray = np.zeros((screensize[1], screensize[0], 3), dtype = 'uint8')
        screenArray[:][:] = backgroundColour
        return screenArray
    
    def get_screenarray_gray(screensize):
        #print("Functions.get_screenarray_gray()")
        if (not screensize):
            return []
        screenArray = np.zeros((screensize[1], screensize[0]), dtype = 'uint8')
        screenArray[:][:] = 0
        return screenArray