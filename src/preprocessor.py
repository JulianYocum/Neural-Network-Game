#!/usr/bin/env python

import cv2
import numpy as np
from PIL import Image
import math
from scipy import ndimage

size = 28, 28
default_save_path = "../data/img_process/"

#im = Image.open("../data/img_stream/20180801_195944.jpg")

# take in PIL image object, process and save, and return processed image object
def process(im):

    w, h = im.size

    if w > h:
        buffer = w - h
        im = im.crop((buffer/2, 0, w - buffer/2, h))
    elif h > w:
        buffer = h - w
        im = im.crop((0, buffer/2, w, h - buffer/2))

    im = im.rotate(-90)
    im.save(default_save_path + "crop.png")

    # resize image, convert to black-white, and rotate
    im = im.resize(size, Image.ANTIALIAS)

    im.save(default_save_path + "resize.png")


    # open image in OpenCV
    gray = cv2.imread(default_save_path + "resize.png", cv2.IMREAD_GRAYSCALE)

    # resize the images and invert it (black background)
    gray = cv2.resize(255 - gray, (28, 28))
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #128

    while np.sum(gray[0]) == 0:
        gray = gray[1:]

    while np.sum(gray[:,0]) == 0:
        gray = np.delete(gray,0,1)

    while np.sum(gray[-1]) == 0:
        gray = gray[:-1]

    while np.sum(gray[:,-1]) == 0:
        gray = np.delete(gray,-1,1)

    rows,cols = gray.shape

    if rows > cols:
        factor = 20.0/rows
        rows = 20
        cols = int(round(cols*factor))
        gray = cv2.resize(gray, (cols,rows))
    else:
        factor = 20.0/cols
        cols = 20
        rows = int(round(rows*factor))
        gray = cv2.resize(gray, (cols, rows))

    colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
    rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))

    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')

    shiftx,shifty = getBestShift(gray)
    shifted = shift(gray,shiftx,shifty)
    gray = shifted

    # save the processed images
    cv2.imwrite(default_save_path + "process.png", gray)

    """
        all images in the training set have an range from 0-1
        and not from 0-255 so we divide our flatten images
        (a one dimensional vector with our 784 pixels)
        to use the same 0-1 based range
        """

    #flatten = gray.flatten() / 255.0
    """
        we need to store the flatten image and generate
        the correct_vals array
        correct_val for the first digit (9) would be
        [0,0,0,0,0,0,0,0,0,1]
        """

#return flatten
    return gray


def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty


def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        try:
            im = Image.open(sys.argv)
            process(sys.argv[1])
        except:
            print "Error opening file" + sys.argv
    else:
        print "Usage:  python -W ignore preprocessor.py [image_save_path]"




