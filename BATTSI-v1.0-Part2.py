# -*- coding: utf-8 -*-
"""
BATTSI version 0.1
-
Standing for
-
Biological Activity Transformation Tool for Small Insects
version 0.1 - Still Script
last modified July 2021
-
Remaining bugs
*

This series of scripts uses the Python computer vision library OpenCV
"""
import cv2
import pandas as pd # and Pandas for data wrangling
"""
Step 2/3 - Well Define
Iterations for well definition

Provide the following information
"""
videoName = "test"  # name of video
sampleSize = 20
"""

PROCEED TO RUN THE SCRIPT

"""
# initialize the well column/row list
nombres = []
for i in range(sampleSize):
    a = 'well-%i' %(i+1)
    nombres.append(a)
#print(nombres)
# now let's initialize the list of reference point 
ref_point = [] 
crop = False
pozos = []

def shape_selection(event, x, y, flags, param): 
    # grab references to the global variables 
    global ref_point, crop
    # if the left mouse button was clicked, record the starting 
    # (x, y) coordinates and indicate that cropping is being performed 
    if event == cv2.EVENT_LBUTTONDOWN: 
        ref_point = [(x, y)]
    # check to see if the left mouse button was released 
    elif event == cv2.EVENT_LBUTTONUP: 
        # record the ending (x, y) coordinates and indicate that 
        # the cropping operation is finished 
        ref_point.append((x, y))
        # draw a rectangle around the region of interest 
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2) 
        cv2.imshow("BATTSI", image)
# read first frame image
videoImage = "firstFrame-"+videoName+".jpg"
image = cv2.imread(videoImage) 
clone = image.copy()
ventana = ""
cv2.namedWindow("BATTSI")
cv2.setMouseCallback("BATTSI", shape_selection)
print("""-----
BATTSI - version 0.1
-
Perez Galvez July 2021
-
Well Define (part 2/3)
-
Define individual wells as Regions of Interest (ROI)
---
    Instructions:
        1 -start click on TOP-LEFT corner
        2 -drag to BOTTOM-RIGHT
        3 -release click
--
      """)
# run for all cases
for i in nombres:
    #llave = cv2.waitKey(1) & 0xFF
    print("-")
    aiuda = """Draw ROI for well {}.
Press 'c' to Confirm
-"""
    
    print(aiuda.format(i))
    # inform of the well to be selected

    # keep looping until the 'q' key is pressed 
    while True: 
        # display the image and wait for a keypress 
        cv2.imshow("BATTSI", image) 
        key = cv2.waitKey(1) & 0xFF
      
        # press 'r' to reset the window 
        if key == ord("r"): 
            image = clone.copy()
      
        # if the 'c' key is pressed, break from the loop 
        elif key == ord("c"): 
            break
        
    #if llave == ord("e"):
        #break
        
    if len(ref_point) == 2: 
        #crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        pozos.append(ref_point)
        print("""Update:
              {} saved with position {}
              Press 'c' to continue""".format(i,ref_point))
        #cv2.imshow("crop_img", crop_img) 
    
        cv2.waitKey(0)

# close all open windows 
cv2.destroyAllWindows()

# record data
wells = []
wells = pd.DataFrame.from_records(pozos, columns =[('x1,y1'),('x2,y2')])
wells['names'] = nombres
wells.to_csv('wells-frame-{}.csv'.format(videoName))
print("""---
work finished
Copy and save the following information after three dashes:
---""")
print(pozos)
