#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
import asyncio

empty = asyncio.Semaphore(10)
full = asyncio.Semaphore(0)
emptyGrey = asyncio.Semaphore(10)
fullGrey = asyncio.Semaphore(0)
mutex = asyncio.Semaphore(0)

extractCount = 0
greyConversionCount = 0
displayCount = 0

def extractFrames(fileName, outputBuffer):
    global extractCount
    while (extractCount<739):
        empty.acquire()
        try:    
            # open video file
            vidcap = cv2.VideoCapture(fileName)

            # read first image
            success,image = vidcap.read()
    
            print("Reading frame {} {} ".format(extractCount, success))
            mutex.acquire()
            try:
                # add the frame to the buffer
                outputBuffer.put(image)
            finally:
                mutex.release()
                
            extractCount += 1
        finally:
            full.release()
    #print("Frame extraction complete")

def greyFrame(inputBuffer,outputBuffer):
    global greyConversionCount
    while (greyConversionCount<739):
    
        full.acquire()
        try:
            print("Converting frame {}".format(greyConversionCount))
    
            mutex.acquire()
            try:
                # get the next frame
                inputFrame = inputBuffer.get()
            finally:
                mutex.release()
            
            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        
            emptyGrey.acquire()
            try:
                mutex.acquire()
                try:
                    # put image into buffer
                    outputBuffer.put(grayscaleFrame)
                finally:
                    mutex.release()
                greyConversionCount += 1
            finally:
                fullGrey.release()
        finally:
            empty.release()
            
def displayFrames(inputBuffer):
    global displayCount
    
    # go through each frame in the buffer until the buffer is empty
    while(displayCount < 739):
        fullGrey.acquire()
        try:
            mutex.acquire()
            try:
                # get the next frame
                inputGreyFrame = inputBuffer.get()
            finally:
                mutex.release()

            print("Displaying frame {}".format(displayCount))        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow("Video", inputGreyFrame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            displayCount += 1
        finally:
            emptyGrey.release()
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
