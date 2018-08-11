#!/usr/bin/env python

import network
import mnist_loader
import pickle

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

net = network.Network([784, 100, 10])

net.SGD(training_data, 30, 10, 3.0, test_data=test_data)

with open('network.pkl', 'wb') as output:  # Overwrites any existing file.
    pickle.dump(net, output, pickle.HIGHEST_PROTOCOL)
