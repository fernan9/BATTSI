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
import numpy as np
import pandas as pd
from time import process_time
from scipy import stats
from matplotlib import pyplot as plt
"""
Step 3/3 - Motion Detect
Motion detection module

The objective is to track activity of flies inside well trays
Activity is measured as movement

Video tracking can be used to estimate activity of flies per well
Absulute difference between frames is used

To succesfully evaluate CT in this setup we should follow:
    - identify flies from background
    - remove noise signal from plastic reflexions
    - assign area to individual flies to generate data
    - plot activity of individual wells along time
    - define threshold of activity
    - return a critical temperature estimate and confidence interval

LOG

- modification on 12/13/2020
Video was dropping at lost frames. This was solved in the past, but not saved.
A conditional was added to indicate the dropped frame.
Also, the lenght of the video is fictional, not general.

- modification on 07/12/2021 - July

Provide the following information
"""
videoName = 'test'  # name of video
cuadros = 24        # frame rate
sampleSize = 20     # number of individuals
pozos = [[(308, 67), (332, 91)], [(336, 66), (363, 93)], [(366, 67), (396, 96)], [(395, 68), (422, 98)], [(302, 96), (333, 123)], [(336, 98), (363, 124)], [(367, 98), (393, 126)], [(394, 98), (419, 127)], [(302, 127), (331, 152)], [(334, 126), (362, 154)], [(363, 125), (390, 153)], [(393, 127), (422, 156)], [(303, 153), (332, 183)], [(332, 155), (363, 182)], [(363, 153), (391, 183)], [(390, 157), (420, 184)], [(301, 183), (331, 211)], [(333, 183), (361, 210)], [(363, 185), (390, 212)], [(390, 184), (420, 214)]]

"""
Below are the sensitivity parameters
"""
blurKernel = 9      # blur kernel 1,3,5,7,9
dilationIter = 3    # dilation iterations 3,5,7,9

"""
PROCEED TO RUN THE SCRIPT

"""
# remember to install MoviePy by typing in Spyder prompt
# conda install -c conda-forge moviepy 

print("""-----
BATTSI - version 0.1
-
Perez Galvez July 2021
-
Motion Detect (part 3/3)
-
Transform video to dataframe
---
Video to run: {}
Frame rate: {}
Sample size: {}
--
      """.format(videoName, cuadros, sampleSize))
#
cap = cv2.VideoCapture('{}.mp4'.format(videoName))
cuadrosTot = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#cap.get(cv2.CAP_PROP_POS_MSEC)
#cap.set(cv2.CV_CAP_PROP_FPS, 15)
salida = [[]]
l2 = []
i = 0
ret, frame1 = cap.read()
ret, frame2 = cap.read()

nombres = []
for i in range(sampleSize):
    a = 'well-%i' %(i+1)
    nombres.append(a)
#
tamano = pozos
# start time flag
t1_start = process_time()
#
while cap.isOpened():
    if ret:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurKernel,blurKernel), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=dilationIter)

        frame1 = frame2
        ret, frame2 = cap.read()
        
        temp2 = []
        
        clone=dilated.copy()
        for j in range(len(pozos)):
            temp = clone[pozos[j][0][1]:pozos[j][1][1],pozos[j][0][0]:pozos[j][1][0]]
            #temp = dilated[pozos[j][0][1]:pozos[j][1][1],pozos[j][0][0]:pozos[j][1][0]]
    
            #tamano = 
            actividad =  np.sum(temp)/(temp.shape[0]*temp.shape[1])
            temp2.append(actividad)
            
            #print(tamano, actividad, i, nombres[j])
        
        salida.append(temp2)
        
        i+=1
        if i % 1000 == 0: print("{} frames analyzed".format(i))
    elif i > cuadrosTot-1 :         # video length should be here
        print(ret)
        break
    else:
        print(ret,i,"drop frame")
        ret, frame2 = cap.read()
        i+=1
    #salida.append(i)
    
print(i)
    
# stop time
t1_stop = process_time()
print("Elapsed time:", t1_stop, t1_start)


cv2.destroyAllWindows()
cap.release()


# Plot of activity traces
df=pd.DataFrame(salida,columns=nombres)
#hist = df.hist(bins=3)
#print(hist)

df['seconds'] = df.index / cuadros
colnames = list(df.columns)
barras = df.plot(x='seconds', y=colnames[:-1], figsize=(5,50),subplots = True)
plt.savefig('activity-{}-k{}-i{}.pdf'.format(videoName,blurKernel,dilationIter))      # k=kernel i=iterations

# Critical temperature analysis
sec = []
for column in df:
    s = df[column].tolist()
    ls = [k for k, e in enumerate(s) if e > 0]
    if len(ls) == 0:
        sec.append(0)
    else:
        sec.append(ls[(len(ls)-1)]/cuadros)

duracion = sec.pop()
print(sec, duracion)
#plt.hist(sec)
stats.describe(sec)
#plt.savefig('activityTrace-254.pdf')

df.to_csv('DataFrame-{}-k{}-i{}.csv'.format(videoName,blurKernel,dilationIter))  # where to save it, usually as a csv

#Then you can load it back using:
#df = pd.read_pickle(file_name)
"""
frame drop CORRECTION
"""
import ffmpeg
probe = ffmpeg.probe('{}.mp4'.format(videoName))
totalSec = probe['streams'][1]['duration']
CTmaxCorr = np.float64(sec)*float(totalSec)/duracion

resultados = {'Well':nombres,'CTmax':sec, 'CTmaxCorr':CTmaxCorr}

dfctmax = pd.DataFrame(resultados)

dfctmax.to_csv('result-{}-k{}-i{}.csv'.format(videoName,blurKernel,dilationIter))
