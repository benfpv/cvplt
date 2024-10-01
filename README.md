# cvplt
cvplt is a function written in Python to easily plot and overlay a Numpy 1D array to an existing Numpy image array (Rows x Columns x Colour[B,G,R]), for the purpose of visualizing plots on images via opencv-python's (i.e., cv2's) imshow().

Notes:
- Data can include np.Nan's - they are simply omitted from plots.
- Singular data points are plotted as points (i.e., cv2.circle() function).
- Pairs of data points are plotted as lines (i.e., cv2.line() function).

![depiction 001](https://github.com/benfpv/cvplt/assets/55154673/b530c88e-9a92-4d31-a2aa-99e7ac4c821c)

# Repository Contents
1. main.py
2. cvplt.py
3. functions_cvplt.py
4. README.md

# Prerequisites
1. Numpy
2. CV2 (opencv-python)

# Instructions to Run the Demo
1. Run main.py with Python.
2. See main.py > Main.loop() for the inputs used to create the demo plots.
3. Expected outcome is that 5 demo plots should be plotted onto a 800x400 window.

![dispArray_Resize](https://github.com/benfpv/cvplt/assets/55154673/5c392636-13fb-45b8-88a1-12eb04732261)

# Instructions for Use
1. Add "cvplt.py" and "functions.py" to your project directory.
2. Install and import numpy and cv2 in the script where you intend to use this.
3. Import "cvplt.py" and "functions.py" in the script (e.g., from cvplt import *, from functions.py import *)
4. Call cvplt.draw_plot() function with the required inputs. Please view "# Functions" section for details.

# Functions
1. draw_plot(renderArray, data, plotBeginXY, plotEndXY, plotTitle="", plotBackgroundColour=[1,1,1], plotOutlineColour=[250,250,250], plotValuesColour=[250,250,250])
  - renderArray: Numpy array (# of Rows, # of Columns, Colour(B,G,R)), a BGR image which you want to add your plot to.
  - data: Numpy array (# of Data Values), 1d Numpy array you wish to plot.
  - plotBeginXY: Numpy array or List (X, Y), XY coordinates of beginning or top-left of plot (inclusive).
  - plotEndXY: Numpy array or List (X, Y), XY coordinates of end or bottom-right of plot (inclusive).
  - plotTitle [Optional]: str, title of the plot you wish to be presented in the top-middle of the plot.
  - plotBackgroundColour [Optional]: Numpy array or List (B,G,R), BGR colour that you want the plot background to be.
  - plotOutlineColour [Optional]: Numpy array or List (B,G,R), BGR colour that you want the plot outline and text to be.
  - plotValuesColour [Optional]: Numpy array or List (B,G,R), BGR colour that you want the plotted data values to be.
