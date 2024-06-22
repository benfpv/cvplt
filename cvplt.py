import numpy as np
import cv2

from functions_cvplt import *

class cvplt:
    def draw_plot_legacy(plotTitle, data, renderArray, plotArrayPosition, plotArraySize, plotBackgroundColour, plotOutlineColour, plotValuesColour):
        #print("cvplt.draw_plot()")
        if not renderArray.any():
            return []
        dataLen = len(data)
        if dataLen < 2:
            return renderArray
        # Create plotArray
        plotArray, plotArraySize = cvplt.plotArray_create(plotArraySize, plotBackgroundColour)
        # Draw plotOutlines on plotArray
        plotArray = cvplt.plotArray_draw_outline(plotArray, plotArraySize, plotOutlineColour)
        # Correct plotArraySize to be within plotOutlines.
        plotArraySizeActual = [plotArraySize[0]-2, plotArraySize[1]-2] #Y axis has additional to account for extra data range and rounding, else plotOutline is compromised by plotted dataValues
        # Process Data
        dataToPlot, dataLenToPlot, dataRange = cvplt.plotArray_process_data(data, dataLen, plotArraySizeActual)
        # Draw plotValues on plotArray (in reverse)
        plotArray = cvplt.plotArray_draw_plot(plotArray, plotArraySizeActual, dataToPlot, dataLenToPlot, plotValuesColour)
        # Draw Text onto plotArray (font position and size may need "tuning" to fit similarly across differently sized plots)
        plotArray = cvplt.plotArray_draw_text(plotTitle, plotArray, plotArraySize, dataRange, plotOutlineColour)
        # Draw plotArray on renderArray
        renderArray = cvplt.draw_plotArray_to_renderArray(plotArray, renderArray, plotArrayPosition, plotArraySize)
        return renderArray
        
    def draw_plot(renderArray, data, plotBeginXY, plotEndXY, plotTitle="", plotBackgroundColour=[1,1,1], plotOutlineColour=[250,250,250], plotValuesColour=[250,250,250]):
        #print("cvplt.draw_plot()")
        if not renderArray.any():
            return []
        dataLen = len(data)
        if dataLen < 2:
            return renderArray
        # Get plotArrayPosition and plotArraySize
        plotBeginXY = np.array(plotBeginXY)
        plotEndXY = np.array(plotEndXY)
        #print("plotBeginXY: {}, plotEndXY: {}".format(plotBeginXY, plotEndXY))
        plotArraySize = np.array(plotEndXY-plotBeginXY, dtype="int")
        #plotArraySize = np.array([plotEndXY[0]-plotBeginXY[0], plotEndXY[1]-plotBeginXY[1]], dtype="int")
        data, dataLen = cvplt.data_resize(data, dataLen, plotArraySize) # RESIZE
        #print("plotArraySize: {}".format(plotArraySize))
        plotArraySizeHalf = np.array(plotArraySize * 0.5, dtype="int")
        #print("plotArraySizeHalf: {}".format(plotArraySizeHalf))
        plotArrayPosition = plotBeginXY + plotArraySizeHalf
        #print("plotArrayPosition: {}".format(plotArrayPosition))
        # Create plotArray
        plotArray, plotArraySize = cvplt.plotArray_create(plotArraySize, plotBackgroundColour)
        # Correct plotArraySize to be within plotOutlines.
        plotArraySizeActual = [plotArraySize[0]-2, plotArraySize[1]-2] #Y axis has additional to account for extra data range and rounding, else plotOutline is compromised by plotted dataValues
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
    
    def data_resize(data, dataLen, plotArraySize): ## WIPWIPWIP - plot nans as zeros?
        #print("- dataLen: {}, plotArraySize[0]: {}".format(dataLen, plotArraySize[0]))
        if (dataLen == plotArraySize[0]):
            return
        else:
            #print("- data [{}]: {}".format(dataLen, data))
            data = data.astype("float32")
            data = cv2.resize(data, [1,plotArraySize[0]])
            dataLen = len(data)
            data = data.reshape(-1)
            #print("- resized data [{}]: {}".format(dataLen, data))
        return data, dataLen
    
    def plotArray_create(plotArraySize, plotBackgroundColour):
        # Create plotArray
        plotArray = Functions.get_screenarray_colour(plotArraySize, plotBackgroundColour)
        plotArraySize = Functions.get_screensize(plotArray)
        #print("- plotArraySize: {}, plotArrayDepth: {}".format(plotArraySize, plotArrayDepth))
        return plotArray, plotArraySize
    
    def plotArray_draw_outline(plotArray, plotArraySize, plotOutlineColour):
        # Draw plotOutlines on plotArray
        plotArray = cv2.rectangle(plotArray, 
                [0, 0],
                [plotArraySize[0]-1, plotArraySize[1]-1],
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
        dataRange = [dataSortedMagnitude[0], dataSortedMagnitude[-1-dataNanCount]]
        dataRangeLen = dataRange[1]-dataRange[0]
        #print("- dataLen: {}, dataNanCount: {}, dataRange: {}, dataRangeLen: {}".format(dataLen, dataNanCount, dataRange, dataRangeLen))
        # Multiply Data Values (Y) to plotArray Y size
        if (plotArraySizeActual[1] % 2 == 0): # Correct if plotArraySize (Y) is even
            dataMultiplier = (plotArraySizeActual[1]-1) / dataRangeLen #Fit within plot outline rectangle
        else:
            dataMultiplier = plotArraySizeActual[1] / dataRangeLen
        #print("- dataMultiplier: {}".format(dataMultiplier))
        dataMultiplied = (data * dataMultiplier)
        # Characterize DataMultiplied
        dataMultipliedSortedMagnitude = dataMultiplied.copy()
        dataMultipliedSortedMagnitude.sort()
        dataMultipliedRange = [int(np.floor(dataMultipliedSortedMagnitude[0])), int(np.ceil(dataMultipliedSortedMagnitude[-1-dataNanCount]))]
        #dataMultipliedRangeLen = dataMultipliedRange[1]-dataMultipliedRange[0]
        #dataMultipliedMedian = np.median(dataMultiplied)
        #print("- dataMultiplier: {}, dataMultipliedRange: {}, dataMultipliedRangeLen: {}, dataMultipliedMedian: {}".format(dataMultiplier, dataMultipliedRange, dataMultipliedRangeLen, dataMultipliedMedian))
        # Correct the To-Plot Data Values to fit to plot
        dataToPlot = dataMultiplied
        if dataMultipliedRange[0] < 0:
            dataToPlot = dataToPlot + np.absolute(dataMultipliedRange[0])
        elif dataMultipliedRange[0] > 0:
            dataToPlot = dataToPlot - dataMultipliedRange[0] - 1
        if (plotArraySizeActual[1] % 2 == 0):
            dataToPlot = dataToPlot + 1
        # Characterize DataToPlot
        #dataToPlotSortedMagnitude = sorted(dataToPlot)
        #dataToPlotRange = [int(np.floor(dataToPlotSortedMagnitude[0])), int(np.ceil(dataToPlotSortedMagnitude[-1]))]
        #dataToPlotRangeLen = dataToPlotRange[1]-dataToPlotRange[0]
        #dataToPlotMedian = np.median(dataToPlot)
        #print("- dataToPlotRange: {}, dataToPlotRangeLen: {}, dataToPlotMedian: {}".format(dataToPlotRange, dataToPlotRangeLen, dataToPlotMedian))
        # Correct Data Length
        dataLenToPlot = dataLen
        if dataLen > plotArraySizeActual[0]:
            dataLenToPlot = plotArraySizeActual[0]
        #print("- dataLenToPlot: {}".format(dataLenToPlot))
        return dataToPlot, dataLenToPlot, dataRange
    
    def plotArray_draw_plot(plotArray, plotArraySizeActual, dataToPlot, dataLenToPlot, plotValuesColour):
        # Draw plotValues on plotArray (in reverse)
        if dataLenToPlot >= 2:
            for i in range(1,dataLenToPlot):
                values = np.array([dataToPlot[-i-1], dataToPlot[-i]])
                coordinates = np.zeros((2,2), dtype="int")
                nanCount = np.count_nonzero(np.isnan(values))
                if nanCount == 0: # Anterior and Posterior are Plotted
                    coordinates[0][0] = plotArraySizeActual[0]-i+1 #Posterior
                    coordinates[0][1] = plotArraySizeActual[1]-int(values[1])
                    coordinates[1][0] = plotArraySizeActual[0]-i #Anterior
                    coordinates[1][1] = plotArraySizeActual[1]-int(values[0])
                    plotArray = cv2.line(plotArray, coordinates[0], coordinates[1], plotValuesColour, 1)
                elif nanCount == 1:
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
            if not np.isnan(dataToPlot):
                coordinates = np.array([0,dataToPlot])
                plotArray = cv2.circle(plotArray, coordinates, radius=0, color=plotValuesColour, thickness=-1)
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
    
    def draw_plotArray_to_renderArray(plotArray, renderArray, plotArrayPosition, plotArraySize):
        # Get renderArray Details
        #renderArraySize = Functions.get_screensize(renderArray)
        #print("- renderArraySize: {}, renderArrayDepth: {}".format(renderArraySize, renderArrayDepth))
        # Determine subset of renderArray to overlay with plotArray
        rowRange = [int(plotArrayPosition[1]-(plotArraySize[1]*.5)), int((plotArrayPosition[1]+plotArraySize[1]*.5))]
        colRange = [int(plotArrayPosition[0]-(plotArraySize[0]*.5)), int((plotArrayPosition[0]+plotArraySize[0]*.5))]
        #print("- rowRange: {}, colRange: {}".format(rowRange, colRange))
        # Draw plotArray on renderArray
        rowCounter = 0
        for row in range(rowRange[0], rowRange[1]):
            colCounter = 0
            for col in range(colRange[0], colRange[1]):
                #print("- row: {}, col: {}".format(row, col))
                #print("- rowCounter: {}, colCounter: {}".format(rowCounter, colCounter))
                renderArray[row][col] = plotArray[rowCounter][colCounter]
                colCounter += 1
            rowCounter += 1
        return renderArray