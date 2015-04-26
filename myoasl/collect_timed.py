# Run application
import time
import argparse
import cPickle
from Tkinter import *
import pyttsx
import numpy as np
import sys
import os 

from myoasl.ml.preprocess import merge_data
from myoasl.myo.myo_raw import MyoRaw

class EMGHandler(object):
    def __init__(self):
        self.data = []
        self.is_recording = False
        self.current_key = None

    def __call__(self, emg, moving, times=[]):
        if self.is_recording:
            self.data.append(emg)

    def start(self):
        self.is_recording = True

    def stop(self):
        self.is_recording = False
        data = np.array(self.data)
        self.data = []
        return data

class IMUHandler(object):
    def __init__(self):
        self.data = []
        self.is_recording = False
        self.current_key = None

    def __call__(self, quat, acc, gyro):
        if self.is_recording:
            self.data.append(list(quat) + list(acc) + list(gyro))

    def start(self):
        self.is_recording = True

    def stop(self):
        self.is_recording = False
        data = np.array(self.data)
        self.data = []
        return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file")
    parser.add_argument('mappings', help='filename of key to sign mapping used'
                                         'to generate data')
    parser.add_argument('--speak', action='store_true')
    parser.add_argument('--tty', type=int, default=None)
    parser.add_argument('--key', required=True)
    parser.add_argument('--num-samples', dest='num_samples', type=int, required=True)

    parser.add_argument('--sign-length', dest="sign_length", type=float,
                        default=1.5)

    args = parser.parse_args()

    # Collect all the sign text
    signs = []
    keys = []
    with open(args.mappings) as fp:
        for line in fp:
            key, sign = line.split(':')
            keys.append(key)
            signs.append(sign.strip())

    emg_handler = EMGHandler()
    imu_handler = IMUHandler()

    def start_recording():
        emg_handler.start()
        imu_handler.start()

    def stop_recording():
        emg_data = [emg_handler.stop()]
        imu_data = [imu_handler.stop()]

        # print emg_data[0].shape
        # print imu_data[0].shape

        with open(args.output_file, 'a') as fp:
            fp.write("%d\t" % keys.index(args.key))
            fp.write(",".join([str(x) for datum in emg_data[0]
                               for x in datum]))
            fp.write("\t")
            fp.write(",".join([str(x) for datum in imu_data[0]
                               for x in datum]))
            fp.write("\n")

    # Connect to Myo Armband
    myo = MyoRaw(tty=args.tty)
    myo.add_emg_handler(emg_handler)
    myo.add_imu_handler(imu_handler)
    myo.connect()

    utterances = [' ']
    for _ in xrange(args.num_samples):
        print 'Prepare for the', signs[keys.index(args.key)]
        time.sleep(1)
        print 'Make the', signs[keys.index(args.key)]

        myo.vibrate(1)
        start_recording()
        start_time = time.time()
        while (time.time() - start_time) < args.sign_length:
            myo.run()

        stop_recording()

if __name__ == "__main__":
    main()
