import myo
import time
import threading
import collections
import csv
import numpy as np


def data_get():

    d_sum = []
    while d_sum.__len__() != 64:
        d_arr = []
        data = listener.get_emg_data()
        dataSet.append(data)
        # data = np.reshape(data, (64, 1))
        d_sum = [item for t in data for item in t]
        d_arr.append(d_sum)
        d_arr = np.array(d_arr)
        time.sleep(0.01)
    return d_arr


class MyListener(myo.DeviceListener):

    def __init__(self, queue_size=8):
        self.lock = threading.Lock()
        self.emg_data_queue = collections.deque(maxlen=queue_size)

    def on_connect(self, device, timestamp, firmware_version):
        device.set_stream_emg(myo.StreamEmg.enabled)

    def on_emg_data(self, device, timestamp, emg_data):
        with self.lock:
            self.emg_data_queue.append(emg_data)

    def get_emg_data(self):
        with self.lock:
            return list(self.emg_data_queue)


#myo.init(dist_path='C:\\Users\\Ahmed\\PycharmProjects\\dataget\\sdk\\bin')
#hub = myo.Hub()
start = time.time()
# temp = []
dataSet = []
name = ''
myo.init(dist_path='C:\\Users\\Ahmed\\PycharmProjects\\dataget\\sdk\\bin')
hub = myo.Hub()
listener = MyListener()
hub.run(2000, listener)
#try:
    #listener = MyListener()
    #hub.run(2000, listener)

    #data_get()

    #name = input('Enter file name')
    #print('Recording to '+name+' started')
    #while True:
       # print(data_get())
#finally:
   # hub.shutdown()

'''
    df = ((dataSet[0][0][0],) + dataSet[0][0][1],)
    for i in range(1, dataSet.__len__()):
        df = df + ((dataSet[i][0][0],) + dataSet[i][0][1],)
    f = open(name+'.csv', 'w', newline='')

    with f:
        writer = csv.writer(f)

        for fr in df:
            writer.writerow(fr)
'''
