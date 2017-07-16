"""
Test to collect data with a 360 controller...
Based on ../1. collect_data.py
"""

from X360DebugWindow import *
from X360DataSource import *

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os

starting_value = 1

BASE_PATH = 'Z:/pygta5/' # for the training data


# In the original collect_data we had 9 spots, we only need 6
# sample training data:
#  LTS_x LTX_y RTS_x RTS_y LRTG RTRG
# [0,    0,    0,    0,    0,   0]
# The thumb stick values range from -1 to 1 and the trigger values from 0 to 1 

while True:
    file_name = BASE_PATH+'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        break

window = X360DebugWindow()
data_source = X360DataSource()

def data_to_save(packet):
    return [
        packet['LTS']['X'],
        packet['LTS']['Y'],
        packet['RTS']['X'],
        packet['RTS']['Y'],
        packet['TRG']['L'],
        packet['TRG']['R']
    ]

def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while(True):
        
        if not paused:
            screen = grab_screen(region=(0,40,1920,1120))
            last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (480,270))
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            
            data_packet = data_source.getLastPacket()
            window.view.updateViewWithPacket(data_packet)
            output = data_to_save(data_packet)
            training_data.append([screen,output])

            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            # cv2.imshow('window',cv2.resize(screen,(640,360)))
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #    cv2.destroyAllWindows()
            #    break

            if len(training_data) % 100 == 0:
                print(len(training_data))
                
                if len(training_data) == 500:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = BASE_PATH+'training_data-{}.npy'.format(starting_value)

                    
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main(file_name, starting_value)