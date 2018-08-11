#!/usr/bin/env python

from preprocessor import process
from collector import capture
from PIL import Image
import numpy as np
import pickle
import random
from subprocess import check_output, call
import glob
import os


def main():
    print "\nWelcome to the Neural Network Guessing Game!"

    random_int = random.randint(0,9)

    # open interface
    interface(random_int)

    # remove images in img_stream
    for im in glob.glob("../data/img_stream/*.jpg"):
        os.remove(im)

    # poweroff screen
    call(['adb','shell','input','keyevent = POWER'])


def interface(computer_num):
    #computer_num = 8     #TEST

    num_of_tries = 0

    print("I have a number from 0 to 9."),

    while(True):

        raw_input("Please write down your guess and press enter...")

        raw_image = capture()
        processed_image = process(raw_image)
        user_num = run_network(processed_image)

        print "\nYour number is: " + str(user_num)
        correct = raw_input("If correct, press enter. If not, press 'n'... ")

        if correct == "n" or correct == "N":
            user_num = handle_wrong_num()

        # if user wants to try again, repeat loop
        if user_num == -1:
            print
            continue

        num_of_tries += 1

        if user_num < computer_num:
            print("\nYour number is less than mine!")
        elif user_num > computer_num:
            print("\nYour number is greater than mine!")
        elif user_num == computer_num:
            break

    if num_of_tries == 0:
        print "\nThanks for playing!\n"
    else:
        if num_of_tries == 1:
            grammar = " try!\n"
        elif num_of_tries > 1:
            grammar = " tries!\n"

        print "\nCongratulations, you won the game in " + str(num_of_tries) + grammar



# take in image object and return number
def run_network(im):

    pixel_array = np.array(im, dtype="float32")
    pixel_array = np.append([], pixel_array)
    pixel_array = np.array([[x/255] for x in pixel_array])

    with open('../data/network.pkl', 'rb') as network_data:
        network = pickle.load(network_data)
        item = network.feedforward(pixel_array)
    #print item
    return item.argmax()
"""
    if max(item) >= .5:
        print "Your number is: " + str(item.argmax())
    else:
        print "I think your number is: " + str(item.argmax())
"""

def handle_wrong_num():
    print "Moving image to data/img_fail/..."

    fl = glob.glob('../data/img_stream/*.jpg')
    last_file = max(fl, key=os.path.getctime)

    im = Image.open(last_file)
    im.save("../data/img_fail/" + os.path.basename(last_file))

    option = raw_input("Would you like to override [1], or try again? [2] or [enter] ")

    while(True):
        if option == '1':
            return int(raw_input("Please enter your number: "))
        elif option == '2' or option == '':
            return -1
        else:
            print "Please select override [1] or try again [2] "


if __name__ == "__main__":
    main()
