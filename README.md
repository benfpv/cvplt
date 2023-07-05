# cvplt
cvplt is a function to plot a 1d Numpy array onto an existing bgr image, such as opencv-python bgr image (i.e., Numpy 3d array (Rows x Columns x Colour(BGR)).
np.Nan's are omitted. 
Singular data points are plotted as points (i.e., cv2.circle() function).
Pairs of data points are plotted as lines (i.e., cv2.line() function).

# Repository Contents
1. main.py
2. cvplt.py
3. functions.py

# Prerequisites
1. Numpy
2. CV2 (opencv-python)

# Instructions to Run the Demo
1. Run main.py with Python.
2. Expected outcome is that 5 demo plots should be plotted onto a 800x800 image resized to, and presented on, a 1600x1600 window.
3. See main.py > Main.loop() for the inputs used to create the demo plots.

# Instructions for Use
1. Add "cvplt.py" and "functions.py" to your project directory.
2. Install and import numpy and cv2 in the script where you intend to use this.
3. Import "cvplt.py" and "functions.py" in the script (e.g., from cvplt import *, from functions.py import *)
4. Call cvplt.draw_plot() function with the required inputs. Please view "# Functions" section for details.

# Functions
1. draw_plot(plotTitle, data, renderArray, plotArrayPosition, plotArraySize, plotBackgroundColour, plotOutlineColour, plotValuesColour)
  - plotTitle, str, title of the plot you wish to be presented in the top-middle of the plot.
  - data, 1d Numpy array (Data Values), 1d Numpy array you wish to plot.
  - renderArray, 3d Numpy array (Rows, Columns, Colour[B,G,R]), a BGR image which you want to add your plot to.
  - plotArrayPosition, 1d Numpy array or List (X, Y), XY coordinates of renderArray where you want the center of your plot to be.
  - plotArraySize, 1d Numpy array or List (X, Y), XY size that you want your plot to be on the renderArray.
  - plotBackgroundColour, 1d Numpy array or List (B,G,R), BGR colour that you want the plot background to be.
  - plotOutlineColour, 1d Numpy array or List (B,G,R), BGR colour that you want the plot outline and text to be.
  - plotValuesColour, 1d Numpy array or List (B,G,R), BGR colour that you want the plotted data values to be.
