from __future__ import absolute_import
from getdata import data_get
from getdata import listener
from getdata import hub
import os
import time
import numpy as np  # linear algebra
import tensorflow as tf
from pickle import load  # to load scaler
import win32com.client as comclt
import win32gui
# noinspection PyUnresolvedReferences
import pandas as pd  # loading data in table form
# noinspection PyUnresolvedReferences
from sklearn.preprocessing import normalize, StandardScaler  # machine learning algorithm library
# noinspection PyUnresolvedReferences
import keras  # library for neural network
# noinspection PyUnresolvedReferences
import datetime
# noinspection PyUnresolvedReferences
from pandas import get_dummies
# noinspection PyUnresolvedReferences
from sklearn.model_selection import train_test_split
# noinspection PyUnresolvedReferences
from tensorflow.keras.models import Sequential
# noinspection PyUnresolvedReferences
from tensorflow.keras.layers import Dense, Dropout
# noinspection PyUnresolvedReferences
from tensorflow.keras.layers import *
# noinspection PyUnresolvedReferences
# Config the matlotlib backend as plotting inline in IPython
from keras.models import load_model  # to load model

'''Code'''
wgui = win32gui

wsh = comclt.Dispatch("WScript.Shell")

scaler = load(open('right_scaler_64.pkl', 'rb'))

model = tf.keras.models.load_model('right_model_64csv.h5')
'''Loading the model'''

print('Model Loaded')
os.startfile("MyoHand")  # open the application


def main():

    """This function checks for the Listening gesture
    then gives a wait time for the user to make the
    wanted gesture. A call for the Emg data is made with
    'getdate' module and sent to the model to predict the
    performed gesture"""

    while listener.read:
        print('Listening..')
        time.sleep(2)

        data = data_get()

        data = data.reshape(1, 64)

        data = scaler.transform(data)

        prediction = model.predict(data)

        predict_label = np.argmax(prediction, axis=1)

        name = wgui.GetWindowText(wgui.GetForegroundWindow())

        if name == 'MyoHand':

            if predict_label == 0:  # if bag 
                print('bag')


            elif predict_label == 1:  # if grab 
                print('grab')


            elif predict_label == 2:  # if pen 
                print('pen')


            elif predict_label == 3:  # if point 
                print('point')

            elif predict_label == 4:  # if rest 
                print('rest')


        listener.read = False


time.sleep(1)
while True:
    main()
    if not bool(wgui.FindWindow(None, 'MyoHand')):  # if window is closed shutdown the hub and end process
        hub.shutdown()
        exit(0)
