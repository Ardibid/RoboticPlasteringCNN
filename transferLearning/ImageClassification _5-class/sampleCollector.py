######################################################################
# ArdavanBidgoli
# CMU School of Architecture
# Robotic Plastering Project
# Feedback-loop image classifier
# Tested with/for:
#   Tensorflow 0.12.1
#   OpenCV 3.2.0-dev
######################################################################


# Imports
######################################################################

# Importing OpenCV and Numpy for image processing
# This line is only necessary if OpenCV doesn't automatically loads
sys.path.append("/usr/local/opt/opencv3/lib/python3.5/site-packages/")
import cv2
import numpy as np

# Import libraries for:
#   System read and write
#   Checking object types
import sys
import os
import shutil
import types

# import os.path methods for file manipulation on the drive
from os.path import isfile, join, exists

# General Variables
######################################################################

# Sets the resolution that will be cropped from the original image 
imageRes = 1200
# Sets the sample resolution 
sampelRes = 300
# Sets the naming standard
scannedFolder = "./scanned"
croppedFolder = "cropped"
tileFolders = "tiles"
croppedNames = "cropped_"
tileNames = "tile_"

# Functions
######################################################################

# Converts single items and 2D lists to 1D lists
# Helper Function
def toList(input):
    if isinstance(input, list) : 
        if isinstance(input[0], list):
            newList = []
            for item in input:
                for subItem in item:
                    newList.append(subItem)
            print (len(newList))
            return(newList)
        return (input)
    else:
        return ([input])

# Reads images from hard disk
def loadImages(folder, grayScale = False):
    # collects all file names
    files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
    # filters only the .jpg files
    names = [f for f in files if f.split(".")[1].lower() == "jpg"]
    size = len(names)
    loadedImages = []
    for i in range (size):
        # generating image name and path
        path = folder+"/"+names[i]
        # read the image
        if grayScale:
            img = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        else:
            img = cv2.imread(path)
        # updating the library
        #image_path.append(path)
        loadedImages.append(img)
    return loadedImages

# Crops the central region of the image for sampling
def cropImage(images):
    croppedImages = []
    # find the cropped coordinations
    for i in range (len(images)):
        h , w, _ = images[i].shape
        xm = w//2
        ym = h//2
        x0 = xm - imageRes//2
        x1 = xm + imageRes//2
        y0 = ym - imageRes//2
        y1 = ym + imageRes//2
        # crop the image
        croppedImg = images[i][y0:y1, x0:x1]
        croppedImages.append(croppedImg)
    return croppedImages

# Converts image to grayscale
def grayScale (images):
    images = toList(images)
    grayScales = []
    for img in images:
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayScales.append(gray_image)
    return grayScales

# Displays image
def showImage(images):
    images = toList(images)
    # displaying the images
    for img in images:
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Save image to specific folder
def saveImage(folder, name, images, clean= False):
    # check if the directory exist
    images = toList(images)
    if not exists(folder):
        print ("Directory doesn't exist, making one!")
        os.makedirs(folder)

    # deletes the old files
    if clean:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except:
                pass

    # iterating over images
    size = len(images)
    for i in range (size):
        # creating the index
        if (i < 10):
            index = "00" + str(i)
        elif (i < 100):
            index = "0"  + str(i)
        else:
            index = str (i)
        # writing the files
        newName = name + index + ".jpg"
        newPath = os.path.join (folder, newName)
        cv2.imwrite(newPath, images[i])

# Tiles the images to make samples
def tileSamples(images):
    images = toList(images)
    size = len(images)
    rows = imageRes//sampelRes
    cols = rows
    tiles = [[] for i in range (size)]
    for i in range(size):
        currentImage = images[i]
        for j in range (rows):
            y0= j * sampelRes
            for k in range (cols):
                x0 = sampelRes*k
                tempImg = currentImage[y0:y0+sampelRes,
                                       x0:x0+sampelRes]
                tiles[i].append(tempImg)
    return tiles

# Saves the tiled samples
def saveTiles(tiles):
    size = len(tiles)
    for i in range(size):       
        if (i < 10):
            index = "00" + str(i)
        elif (i < 100):
            index = "0"  + str(i)
        else:
            index = str (i)

        newName = tileNames+str(i)+"_"
        saveImage(tileFolders,newName, tiles[i])

# main body of the code!  
images = loadImages(scannedFolder)
cropped = cropImage(images)
grayImages = grayScale(cropped)
tiled = tileSamples(grayImages)
showImage(tiled)
saveTiles(tiled)

# save the images
#saveImage("this", "name")
 





