import numpy as np
import cv2

class cvplt:
    ### Direct Usage Functions ###
    def draw_plot(data, renderArray=None, plotBeginXY=None, plotEndXY=None, plotTitle="", plotBackgroundColour=[2,2,2], plotOutlineColour=[250,250,250], plotValuesColour=[250,250,250]):
        # Plots 1d data onto 2d array
        # Assume renderArray is numpy array > size 2x2.
        # Assume data is 1D numpy array
        dataLen = len(data)
        dataCount = np.count_nonzero(~np.isnan(data))
        # Create renderArray if none provided
        if (renderArray is None):
            dataMin = np.nanmin(data)
            dataMax = np.nanmax(data)
            dataLenForRenderArray = np.nanmax([640, dataLen])
            dataRange = np.nanmax([480, np.ceil(abs(dataMax - dataMin))])
            renderArraySize = np.array([dataLenForRenderArray, dataRange], dtype="int")
            renderArray = cvplt.get_screenarray_colour(renderArraySize, plotBackgroundColour)
        # Return Conditions
        if ((dataLen < 1) or (dataCount < 1)): # Currently assumes dataLen > 0, since it draws lines.
            return renderArray
        # Determine Grayscale or Colour
        renderArrayShapeLen = len(renderArray.shape)
        if (renderArrayShapeLen == 2):
            grayOrColour = False
        elif (renderArrayShapeLen == 3):
            grayOrColour = True
        else:
            return renderArray
        # Convert Colours if necessary
        if (grayOrColour == False):
            if (isinstance(plotBackgroundColour, (np.ndarray, int)) == False):
                plotBackgroundColour = int(np.mean(plotBackgroundColour))
            if (isinstance(plotOutlineColour, (np.ndarray, int)) == False):
                plotOutlineColour = int(np.mean(plotOutlineColour))
            if (isinstance(plotValuesColour, (np.ndarray, int)) == False):
                plotValuesColour = int(np.mean(plotValuesColour))
        else:
            if (isinstance(plotBackgroundColour, (np.ndarray, int)) == True):
                plotBackgroundColour = np.array([plotBackgroundColour] * 3, dtype="int")
            if (isinstance(plotOutlineColour, (np.ndarray, int)) == True):
                plotOutlineColour = np.array([plotOutlineColour] * 3, dtype="int")
            if (isinstance(plotValuesColour, (np.ndarray, int)) == True):
                plotValuesColour = np.array([plotValuesColour] * 3, dtype="int")
        # Get plotArrayPosition and plotArraySize
        if ((plotBeginXY == None) or (plotEndXY == None)):
            plotBeginXY = np.zeros(2, dtype="int")
            plotEndXY = cvplt.get_screensize(renderArray)
        plotBeginXY = np.array(plotBeginXY)
        plotEndXY = np.array(plotEndXY)
        plotArraySize = np.array(plotEndXY-plotBeginXY, dtype="int")
        data, dataLen = cvplt.data_resize(data, dataLen, plotArraySize) # RESIZE
        plotArraySizeHalf = np.array(plotArraySize * 0.5, dtype="int")
        plotArrayPosition = plotBeginXY + plotArraySizeHalf
        # Create plotArray
        plotArray, plotArraySize = cvplt.plotArray_create(plotArraySize, grayOrColour, plotBackgroundColour)
        # Correct plotArraySize to be within plotOutlines.
        plotArraySizeActual = np.array([plotArraySize[0]-2, plotArraySize[1]-2]) #Y axis has additional to account for extra data range and rounding, else plotOutline is compromised by plotted dataValues
        # Process Data
        dataToPlot, dataLenToPlot, dataRange = cvplt.plotArray_process_data(data, dataLen, plotArraySizeActual)
        # Draw plotValues on plotArray (in reverse)
        plotArray = cvplt.plotArray_draw_plot(plotArray, plotArraySizeActual, dataToPlot, dataLenToPlot, plotValuesColour)
        # Draw Text onto plotArray (font position and size may need "tuning" to fit similarly across differently sized plots)
        plotArray = cvplt.plotArray_draw_text(plotTitle, plotArray, plotArraySize, dataRange, plotOutlineColour)
        # Draw plotOutlines on plotArray
        plotArray = cvplt.plotArray_draw_outline(plotArray, plotArraySize, plotOutlineColour)
        # Draw plotArray on renderArray
        renderArray = cvplt.draw_plotArray_to_renderArray(plotArray, renderArray, plotArrayPosition, plotArraySize)
        return renderArray
        
    def draw_plot_coords(data, renderArray=None, connectDots=False, plotBeginXY=None, plotEndXY=None, plotTitle="", plotBackgroundColour=[2,2,2], plotOutlineColour=[250,250,250], plotValuesColour=[250,250,250]):
        # Plots 2d data (coordinates) onto 2d array
        # Assume renderArray is numpy array > size 2x2.
        # Assume data is numpy array of coords, where no coord is nan, but coords can be negative/positive.
        dataLen = len(data)
        dataCount = np.count_nonzero(~np.isnan(data))
        # Create renderArray if none provided
        if (renderArray is None):
            dataMinX = min(data, key=lambda x: x[0])[0]
            dataMinY = min(data, key=lambda x: x[1])[1]
            dataMaxX = max(data, key=lambda x: x[0])[0]
            dataMaxY = max(data, key=lambda x: x[1])[1]
            dataRangeX = np.nanmax([640, np.ceil(abs(dataMaxX - dataMinX))])
            dataRangeY = np.nanmax([480, np.ceil(abs(dataMaxY - dataMinY))])
            renderArraySize = np.array([dataRangeX, dataRangeY], dtype="int")
            renderArray = cvplt.get_screenarray_colour(renderArraySize, plotBackgroundColour)
        # Determine Grayscale or Colour
        renderArrayShapeLen = len(renderArray.shape)
        if (renderArrayShapeLen == 2):
            grayOrColour = False
        elif (renderArrayShapeLen == 3):
            grayOrColour = True
        else:
            return renderArray
        # Convert Colours if necessary
        if (grayOrColour == False):
            if (isinstance(plotBackgroundColour, (np.ndarray, int)) == False):
                plotBackgroundColour = int(np.mean(plotBackgroundColour))
            if (isinstance(plotOutlineColour, (np.ndarray, int)) == False):
                plotOutlineColour = int(np.mean(plotOutlineColour))
            if (isinstance(plotValuesColour, (np.ndarray, int)) == False):
                plotValuesColour = int(np.mean(plotValuesColour))
        else:
            if (isinstance(plotBackgroundColour, (np.ndarray, int)) == True):
                plotBackgroundColour = np.array([plotBackgroundColour] * 3, dtype="int")
            if (isinstance(plotOutlineColour, (np.ndarray, int)) == True):
                plotOutlineColour = np.array([plotOutlineColour] * 3, dtype="int")
            if (isinstance(plotValuesColour, (np.ndarray, int)) == True):
                plotValuesColour = np.array([plotValuesColour] * 3, dtype="int")
        # Get plotArrayPosition and plotArraySize
        if ((plotBeginXY == None) or (plotEndXY == None)):
            plotBeginXY = np.zeros(2, dtype="int")
            plotEndXY = cvplt.get_screensize(renderArray)
        plotBeginXY = np.array(plotBeginXY)
        plotEndXY = np.array(plotEndXY)
        plotArraySize = np.array(plotEndXY-plotBeginXY, dtype="int")
        # Resize Data according to DataTotalSize
        plotArraySizeHalf = np.array(plotArraySize * 0.5, dtype="int")
        plotArrayPosition = plotBeginXY + plotArraySizeHalf
        # Create plotArray
        plotArray, plotArraySize = cvplt.plotArray_create(plotArraySize, grayOrColour, plotBackgroundColour)
        # Correct plotArraySize to be within plotOutlines.
        plotArraySizeActual = np.array([plotArraySize[0]-2, plotArraySize[1]-2]) #Y axis has additional to account for extra data range and rounding, else plotOutline is compromised by plotted dataValues
        # Resize Coordinates 
        data, dataRange, dataSize, dataBufferSize, dataTotalSize = cvplt.data_resize_calibrate_coords(data, plotArraySizeActual) # RESIZE COORDS
        # Draw plotValues on plotArray (in reverse)
        plotArray = cvplt.plotArray_draw_plot_coords(plotArray, plotArraySizeActual, data, dataBufferSize, connectDots, plotValuesColour)
        # Draw Text onto plotArray (font position and size may need "tuning" to fit similarly across differently sized plots)
        plotArray = cvplt.plotArray_draw_text_coords(plotTitle, plotArray, plotArraySize, dataRange, plotOutlineColour)
        # Draw plotOutlines on plotArray
        plotArray = cvplt.plotArray_draw_outline(plotArray, plotArraySize, plotOutlineColour)
        # Draw plotArray on renderArray
        renderArray = cvplt.draw_plotArray_to_renderArray(plotArray, renderArray, plotArrayPosition, plotArraySize)
        return renderArray
    
    ### Supportive Functions ###
    # Common Functions
    def get_screensize(screenshot):
        screenshape = screenshot.shape
        screensize = np.array([screenshape[1], screenshape[0]], dtype="int")
        return screensize

    def get_screencenter(screensize):
        screencenter = (int(screensize[0]*0.5), int(screensize[1]*0.5))
        return screencenter
    
    def get_screenarray_gray(screensize, backgroundColour):
        if (isinstance(backgroundColour, (np.ndarray, int)) == False):
            backgroundColour = np.mean(backgroundColour)
        screenArray = np.zeros((screensize[1], screensize[0]), dtype = 'uint8')
        screenArray[:][:] = backgroundColour
        return screenArray

    def get_screenarray_colour(screensize, backgroundColour):
        if (isinstance(backgroundColour, (np.ndarray, int)) == True):
            backgroundColour = np.array([backgroundColour] * 3, dtype="int")
        screenArray = np.zeros((screensize[1], screensize[0], 3), dtype = 'uint8')
        screenArray[:][:] = backgroundColour
        return screenArray
    
    # Plot-Related Functions
    def data_resize(data, dataLen, plotArraySize):
        if (dataLen == plotArraySize[0]):
            return data, dataLen
        data = data.astype("float32")
        data = cv2.resize(data, [1,plotArraySize[0]])
        dataLen = len(data)
        data = data.reshape(-1)
        return data, dataLen
    
    def data_resize_calibrate_coords(data, plotArraySize):
        # Find bounds for data (min/max coordinates)
        dataMinX = min(data, key=lambda x: x[0])[0]
        dataMinY = min(data, key=lambda x: x[1])[1]
        dataMaxX = max(data, key=lambda x: x[0])[0]
        dataMaxY = max(data, key=lambda x: x[1])[1]
        dataRange = np.array([[dataMinX, dataMinY],[dataMaxX, dataMaxY]], dtype="int")
        dataSizeX = dataMaxX - dataMinX
        dataSizeY = dataMaxY - dataMinY
        dataSize = np.array([dataSizeX, dataSizeY], dtype = "int")
        # Determine appropriate buffer based on min/max coordinates
        dataBufferSingle = np.max([int(dataSizeX * 0.1), int(dataSizeY * 0.1)]) # Buffer at each end (i.e., min-buffer, max+buffer)
        dataBufferSize = np.array([dataBufferSingle, dataBufferSingle], dtype="int")
        dataTotalSizeX = dataSizeX + (dataBufferSingle * 2)
        dataTotalSizeY = dataSizeY + (dataBufferSingle * 2)
        dataTotalSize = np.array([dataTotalSizeX, dataTotalSizeY], dtype="int")
        # Multipliers
        dataMultiplierX = plotArraySize[0] / dataTotalSize[0]
        dataMultiplierY = plotArraySize[1] / dataTotalSize[1]
        dataMultipliers = np.array([dataMultiplierX, dataMultiplierY], dtype="float")
        ### Resize Data Coords & Simultaneously Calibrate to 0,0 + ###
        dataCorrection = np.array([-dataMinX, -dataMinY], dtype="int")
        for c, coord in enumerate(data):
            data[c] = (coord + dataCorrection) * dataMultipliers
        # Find bounds for NEW data
        newDataBufferSize = (dataBufferSize * dataMultipliers).astype(int)
        dataMinX = min(data, key=lambda x: x[0])[0]
        dataMinY = min(data, key=lambda x: x[1])[1]
        dataMaxX = max(data, key=lambda x: x[0])[0]
        dataMaxY = max(data, key=lambda x: x[1])[1]
        # Finalize Bounds
        dataSizeX = dataMaxX - dataMinX
        dataSizeY = dataMaxY - dataMinY
        newDataSize = np.array([dataSizeX, dataSizeY], dtype = "int")
        newDataTotalSizeX = dataSizeX + (newDataBufferSize[0] * 2)
        newDataTotalSizeY = dataSizeY + (newDataBufferSize[1] * 2)
        newDataTotalSize = np.array([newDataTotalSizeX, newDataTotalSizeY], dtype="int")
        return data, dataRange, newDataSize, newDataBufferSize, newDataTotalSize
        
    def plotArray_create(plotArraySize, grayOrColour, plotBackgroundColour):
        # Create plotArray
        if (grayOrColour == False):
            plotArray = cvplt.get_screenarray_gray(plotArraySize, plotBackgroundColour)
        else:
            plotArray = cvplt.get_screenarray_colour(plotArraySize, plotBackgroundColour)
        plotArraySize = cvplt.get_screensize(plotArray)
        return plotArray, plotArraySize
    
    def plotArray_draw_outline(plotArray, plotArraySize, plotOutlineColour):
        # Draw plotOutlines on plotArray
        plotArray = cv2.rectangle(plotArray, 
                np.array([0, 0]),
                np.array([plotArraySize[0]-1, plotArraySize[1]-1]),
                plotOutlineColour, 1)
        return plotArray
    
    def plotArray_process_data(data, dataLen, plotArraySizeActual):
        # Characterize Data
        dataNanCount = np.count_nonzero(np.isnan(data))
        dataSortedMagnitude = data.copy()
        dataSortedMagnitude.sort()
        dataLenToPlot = dataLen
        if dataLen > plotArraySizeActual[0]:
            dataLenToPlot = plotArraySizeActual[0]
        dataRange = np.array([dataSortedMagnitude[0], dataSortedMagnitude[-1-dataNanCount]])
        dataRangeLen = dataRange[1]-dataRange[0]
        # Multiply Data Values (Y) to plotArray Y size
        if (dataRangeLen < 1):
            dataMultiplier = 1
        else:
            if (plotArraySizeActual[1] % 2 == 0): # Correct if plotArraySize (Y) is even
                dataMultiplier = (plotArraySizeActual[1]-1) / dataRangeLen #Fit within plot outline rectangle
            else:
                dataMultiplier = plotArraySizeActual[1] / dataRangeLen
        dataMultiplied = (data * dataMultiplier)
        # Characterize DataMultiplied
        dataMultipliedSortedMagnitude = dataMultiplied.copy()
        dataMultipliedSortedMagnitude.sort()
        dataMultipliedRange = [int(np.floor(dataMultipliedSortedMagnitude[0])), int(np.ceil(dataMultipliedSortedMagnitude[-1-dataNanCount]))]
        # Correct the To-Plot Data Values to fit to plot
        dataToPlot = dataMultiplied
        if (dataMultipliedRange[0] < 0):
            dataToPlot = dataToPlot + np.absolute(dataMultipliedRange[0])
        elif (dataMultipliedRange[0] > 0):
            dataToPlot = dataToPlot - dataMultipliedRange[0] - 1
        if (plotArraySizeActual[1] % 2 == 0):
            dataToPlot = dataToPlot + 1
        # Correct Data Length
        dataLenToPlot = dataLen
        if (dataLen > plotArraySizeActual[0]):
            dataLenToPlot = plotArraySizeActual[0]
        return dataToPlot, dataLenToPlot, dataRange
    
    def plotArray_draw_plot(plotArray, plotArraySizeActual, dataToPlot, dataLenToPlot, plotValuesColour):
        # Draw plotValues on plotArray (in reverse)
        if (dataLenToPlot > 1):
            for i in range(1,dataLenToPlot):
                values = np.array([dataToPlot[-i-1], dataToPlot[-i]])
                coordinates = np.zeros((2,2), dtype="int")
                nanCount = np.count_nonzero(np.isnan(values))
                if (nanCount == 0): # Anterior and Posterior are Plotted
                    coordinates[0][0] = plotArraySizeActual[0]-i+1 #Posterior
                    coordinates[0][1] = plotArraySizeActual[1]-int(values[1])
                    coordinates[1][0] = plotArraySizeActual[0]-i #Anterior
                    coordinates[1][1] = plotArraySizeActual[1]-int(values[0])
                    plotArray = cv2.line(plotArray, coordinates[0], coordinates[1], plotValuesColour, 1)
                elif (nanCount == 1):
                    if np.isnan(values[0]): #Anterior is plotted
                        coordinates[1][0] = plotArraySizeActual[0]-i+1
                        coordinates[1][1] = plotArraySizeActual[1]-int(values[1])
                        plotArray = cv2.circle(plotArray, coordinates[1], radius=0, color=plotValuesColour, thickness=1)
                    else: #Posterior is plotted
                        coordinates[0][0] = plotArraySizeActual[0]-i
                        coordinates[0][1] = plotArraySizeActual[1]-int(values[0])
                        plotArray = cv2.circle(plotArray, coordinates[0], radius=0, color=plotValuesColour, thickness=1)
                else:
                    pass
        else:
            if (not np.isnan(dataToPlot)):
                dotSize = int(np.nanmax([plotArraySizeActual * 0.2, 1]))
                coordinates = np.array([0,dataToPlot])
                plotArray = cv2.circle(plotArray, coordinates, radius=dotSize, color=plotValuesColour, thickness=-1)
        return plotArray
    
    def plotArray_draw_plot_coords(plotArray, plotArraySizeActual, data, dataBufferSize, connectDots, plotValuesColour):
        dotSize = int(np.nanmax([plotArraySizeActual[0] * 0.015, plotArraySizeActual[1] * 0.015, 1]))
        # Plot Dots Coords
        coordinates = np.zeros(2, dtype="int")
        for i, coord in enumerate(data):
            coordinates[0] = coord[0]+dataBufferSize[0]
            coordinates[1] = coord[1]+dataBufferSize[1]
            plotArray = cv2.circle(plotArray, coordinates, radius=dotSize, color=plotValuesColour, thickness=-1)
        # Connect Dots if applicable
        if (connectDots == True):
            pass
        return plotArray
    
    def plotArray_draw_text(plotTitle, plotArray, plotArraySize, dataRange, plotOutlineColour):
        # Draw Text onto plotArray (font position and size may need "tuning" to fit similarly across differently sized plots)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontPositionTuningTop = int(.03 * plotArraySize[1])
        fontPositionTuningBot = int(.007 * plotArraySize[1])
        fontSizeTuning = (.001 * plotArraySize[1])
        # putText Title
        textTitle = plotTitle
        # putText Max
        textMax = "{}  |  {}".format(round(dataRange[1],4), textTitle)
        plotArray = cv2.putText(plotArray, textMax, [3, 11 + fontPositionTuningTop], font, .4 + fontSizeTuning, plotOutlineColour, 1)
        # putText Min
        textMin = "{}".format(round(dataRange[0],4))
        plotArray = cv2.putText(plotArray, textMin, [3, plotArraySize[1]-5 - fontPositionTuningBot], font, .4 + fontSizeTuning, plotOutlineColour, 1)
        return plotArray
    
    def plotArray_draw_text_coords(plotTitle, plotArray, plotArraySize, dataRange, plotOutlineColour):
        # Draw Text onto plotArray (font position and size may need "tuning" to fit similarly across differently sized plots)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontPositionTuningTop = int(.03 * plotArraySize[1])
        fontPositionTuningBot = int(.007 * plotArraySize[1])
        fontSpaceTuning = (.001 * plotArraySize[0])
        fontSizeTuning = (.001 * plotArraySize[1])
        # putText Title
        textTitle = plotTitle
        # putText Max
        textMax = "({},{})  |  {}".format(round(dataRange[0][0],4), round(dataRange[0][1],4), textTitle)
        plotArray = cv2.putText(plotArray, textMax, [3, 11 + fontPositionTuningTop], font, .4 + fontSizeTuning, plotOutlineColour, 1)
        # putText Min
        textMin = "({},{})".format(round(dataRange[1][0],4), round(dataRange[1][1],4))
        plotArray = cv2.putText(plotArray, textMin, [3, plotArraySize[1]-5 - fontPositionTuningBot], font, .4 + fontSizeTuning, plotOutlineColour, 1)
        return plotArray
    
    def draw_plotArray_to_renderArray(plotArray, renderArray, plotArrayPosition, plotArraySize):
        # Determine subset of renderArray to overlay with plotArray
        rowRange = np.array([int(plotArrayPosition[1]-(plotArraySize[1]*.5)), int((plotArrayPosition[1]+plotArraySize[1]*.5))])
        colRange = np.array([int(plotArrayPosition[0]-(plotArraySize[0]*.5)), int((plotArrayPosition[0]+plotArraySize[0]*.5))])
        # Draw plotArray on renderArray
        rowCounter = 0
        for row in range(rowRange[0], rowRange[1]):
            colCounter = 0
            for col in range(colRange[0], colRange[1]):
                renderArray[row][col] = plotArray[rowCounter][colCounter]
                colCounter += 1
            rowCounter += 1
        return renderArray