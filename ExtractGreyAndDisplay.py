#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue

def extractFrames(fileName, outputBuffer):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print("Reading frame {} {} ".format(count, success))
    while success:
        
        # add the frame to the buffer
        outputBuffer.put(image)
       
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1

    print("Frame extraction complete")

def greyFrame(inputBuffer,outputBuffer):
    
    count = 0
    
    while not inputBuffer.empty():
        print("Converting frame {}".format(count))
    
        # get the next frame
        inputFrame = inputBuffer.get()

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        
        #jpgImage = cv2.imencode('.jpg', grayscaleFrame)
        
        # econde frame to base 64
        #jpgAsText = base64.b64encode(jpgImage)
        
        
        
        # put image into buffer
        outputBuffer.put(grayscaleFrame)
        
        count += 1

def displayFrames(inputBuffer):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while not inputBuffer.empty():
        # get the next frame
        inputGreyFrame = inputBuffer.get()
        
        #jpgRawImage = base64.b64decode(inputGreyFrame)

        # convert the raw frame to a numpy array
        #jpgImage = np.asarray(bytearray(inputGreyFrame), dtype=np.uint8)
        
        # get a jpg encoded frame
        #img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", inputGreyFrame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()

# filename of clip to load
filename = 'clip.mp4'

# shared queue  
extractionQueue = queue.Queue()

greyExtractionQueue = queue.Queue()

# extract the frames
extractFrames(filename,extractionQueue)

#grey the Frames
greyFrame(extractionQueue,greyExtractionQueue)

# display the frames
displayFrames(greyExtractionQueue)
