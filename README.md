# cvplt
cvplt is a function to plot a 1d Numpy array onto an existing bgr image, such as opencv-python bgr image (i.e., # of Rows x # of Columns x Colour(B,G,R)).
np.Nan's are omitted. 
Singular data points are plotted as points (i.e., cv2.circle() function).
Pairs of data points are plotted as lines (i.e., cv2.line() function).
![depiction 001](https://github.com/benfpv/cvplt/assets/55154673/b530c88e-9a92-4d31-a2aa-99e7ac4c821c)

# Repository Contents
1. main.py
2. cvplt.py
3. functions.py

# Prerequisites
1. Numpy
2. CV2 (opencv-python)

# Instructions to Run the Demo
1. Run main.py with Python.
2. See main.py > Main.loop() for the inputs used to create the demo plots.
3. Expected outcome is that 5 demo plots should be plotted onto a 800x800 image resized to, and presented on, a 1600x1600 window.
<img width="500" alt="Screen Shot 2023-07-05 at 11 31 46 PM" src="https://github.com/benfpv/cvplt/assets/55154673/df4e022a-a42e-448b-a060-beec2d7ba751">

# Instructions for Use
1. Add "cvplt.py" and "functions.py" to your project directory.
2. Install and import numpy and cv2 in the script where you intend to use this.
3. Import "cvplt.py" and "functions.py" in the script (e.g., from cvplt import *, from functions.py import *)
4. Call cvplt.draw_plot() function with the required inputs. Please view "# Functions" section for details.

# Functions
1. draw_plot(plotTitle, data, renderArray, plotArrayPosition, plotArraySize, plotBackgroundColour, plotOutlineColour, plotValuesColour)
  - plotTitle, str, title of the plot you wish to be presented in the top-middle of the plot.
  - data, Numpy array (# of Data Values), 1d Numpy array you wish to plot.
  - renderArray, Numpy array (# of Rows, # of Columns, Colour(B,G,R)), a BGR image which you want to add your plot to.
  - plotArrayPosition, Numpy array or List (X, Y), XY coordinates of renderArray where you want the center of your plot to be.
  - plotArraySize, Numpy array or List (X, Y), XY size that you want your plot to be on the renderArray.
  - plotBackgroundColour, Numpy array or List (B,G,R), BGR colour that you want the plot background to be.
  - plotOutlineColour, Numpy array or List (B,G,R), BGR colour that you want the plot outline and text to be.
  - plotValuesColour, Numpy array or List (B,G,R), BGR colour that you want the plotted data values to be.
