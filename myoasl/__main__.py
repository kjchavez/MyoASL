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
    parser.add_argument('classifier', help="filename of saved classifier")
    parser.add_argument('mappings', help='filename of key to sign mapping used'
                                         'to generate data')
    parser.add_argument('--speak', action='store_true')
    parser.add_argument('--tty', type=int, default=None)
    parser.add_argument('--sign-length', dest="sign_length", type=float,
                        default=1.0)

    args = parser.parse_args()

    # Collect all the sign text
    signs = []
    with open(args.mappings) as fp:
        for line in fp:
            key, sign = line.split(':')
            signs.append(sign.strip())

    # Load classifier
    with open(args.classifier) as fp:
        classifier = cPickle.load(fp)

    # Text-to-speech initialization
    if args.speak and 'darwin' not in sys.platform:
        engine = pyttsx.init()

    emg_handler = EMGHandler()
    imu_handler = IMUHandler()

    def start_recording():
        emg_handler.start()
        imu_handler.start()

    def stop_recording():
        emg_data = [emg_handler.stop()]
        imu_data = [imu_handler.stop()]

        X = merge_data(emg_data, imu_data, series_length=50)
        label = classifier.predict(X)
        return signs[label]

    # Connect to Myo Armband
    myo = MyoRaw(tty=args.tty)
    myo.add_emg_handler(emg_handler)
    myo.add_imu_handler(imu_handler)
    myo.connect()

    utterances = [' ']
    while True:
        print 'Prepare for the motion'
        time.sleep(1)
        print 'Make the motion'

        myo.vibrate(1)
        start_recording()
        start_time = time.time()
        while (time.time() - start_time) < args.sign_length:
            myo.run()

        sign = stop_recording()
        print sign
        if sign == 'random':
            continue
        if sign != 'stop':
            if utterances[-1] != sign:
                utterances.append(sign)
        else:
            if args.speak :
                if 'darwin' in sys.platform:
                    os.system('say -v \'oliver\' "'+' '.join(utterances).lower()+'" -r 50')
                else:
                    engine.say(' '.join(utterances))
                    engine.runAndWait()
            utterances = [' ']

if __name__ == "__main__":
    main()
