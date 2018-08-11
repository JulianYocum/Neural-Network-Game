#!/usr/bin/env python

from preprocessor import process
from collector import capture
from PIL import Image
import numpy as np
import pickle


def main(image):
    # open interface
    interface()

#image = Image.open("../data/img_stream/20180802_115324.jpg")    #TEST

    # process photo. save processed photo in data/process_img/. return readable numpy array
    image = process(image)

    # send into neural network and return number
    num = run_network(image)

    # send output to user
    output(num)


def interface():
    pass


# take in image object and return number
def run_network(im):

    pixel_array = np.array(im, dtype="float32")
    pixel_array = np.append([], pixel_array)
    pixel_array = np.array([[x/255] for x in pixel_array])

    with open('../data/network.pkl', 'rb') as network_data:
        network = pickle.load(network_data)
        item = network.feedforward(pixel_array)
    print item

    return item.argmax()


def output(n):
    print "Your number is: " + str(n)




if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        im = Image.open(sys.argv[1])
        main(im)

    elif len(sys.argv) == 1:
        im = capture()
        main(im)

    else:
        print "Usage:  ./simple_app.py [path_for_image]"
