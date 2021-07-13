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
"""
Step 1/3 - First Frame
Here we will define individual positions of the insects in the video

We will need to know which video to analyze
"""
videoName = 'Aphid HKD plate'  # type the name of video
"""
As well as the address in your computer
"""
pos = "C:\\Users\\Rodrigo Perez\\OneDrive - University of Kentucky\ThermoFly2021\\Data-TKD\\"
#pos = "C:\\Users\\Rodrigo Perez\\OneDrive - University of Kentucky\\BATTSI\\Test\\"
# example
# pos = "C:\\Users\\frpe222\\OneDrive - University of Kentucky\\BATTSI\\Test\\"
# NOTE the double back slash between folder files
"""
We will define a function that will capture the first frame of your video
"""
# Function to extract frames 
def FrameCapture(path): 
    # Path to video file 
    vidObj = cv2.VideoCapture(path)
    # checks whether frames were extracted 
    success = 1
    while success:
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read()
        # Saves the frames with frame-count
        newVid = "firstFrame-{}.jpg".format(videoName)
        cv2.imwrite(newVid, image)
        print(newVid)
        break
"""
An then run the driver code
"""
# Driver Code 
if __name__ == '__main__': 
    # Calling the function
    #FrameCapture("C:\\Users\\frpe222\\Desktop\\00.Video\\254-15112019.mp4")
    #C:\Users\Rodrigo Perez\OneDrive - University of Kentucky\BATTSI\Test
    posVid = pos+videoName+".mp4"
    FrameCapture(posVid)
"""
Fernan Rodrigo Perez Galvez 2021
COPYRIGHT


don't forget!


"""    