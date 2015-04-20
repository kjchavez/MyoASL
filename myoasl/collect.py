import os
import random
import argparse
from myoasl.myo.myo_raw import MyoRaw
from Tkinter import *

current_key = None
data_stream = []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file")
    parser.add_argument("--signs_file", default="myoasl/mappings.txt")
    parser.add_argument("--tty", type=int, default=None)
    parser.add_argument("--no-myo", dest="no_myo", action="store_true")

    args = parser.parse_args()

    # Read in signs and corresponding keys
    keys = []
    signs = []
    with open(args.signs_file) as fp:
        for line in fp:
            key, sign = line.split(':')
            keys.append(key.strip())
            signs.append(sign.strip())

    key_to_sign = dict(zip(keys, signs))

    def process_emg(emg, moving, times=[]):
        """Handler for emg data"""
        global current_key
        global data_stream
        if current_key:
            data_stream.append(emg)

    def process_imu(quat, acc, gyro):
        print "quat", quat
        print "acc", acc
        print "gyro", gyro
        print "-----"

    if not args.no_myo:
        myo = MyoRaw(tty=args.tty)
        myo.add_emg_handler(process_emg)
        myo.add_imu_handler(process_imu)
        myo.connect()

    # Disable repeat trigger of keypress events
    os.system('xset r off')
    root = Tk()

    def keyup(e):
        global current_key
        global data_stream
        print 'end', key_to_sign.get(current_key, "N/A")
        if current_key in keys:
            with open(args.output_file, 'a') as fp:
                fp.write("%d\t" % keys.index(current_key))
                fp.write(",".join([str(x) for datum in data_stream
                                   for x in datum]))
                fp.write("\n")

        # Reset
        current_key = None
        data_stream = []

    def keydown(e):
        global current_key
        if current_key is None:
            current_key = e.char
        print 'start', key_to_sign.get(current_key, "N/A")

    def random_emg():
        """ Simulate Myo device by generating data every 5 milliseconds"""
        emg = [random.randint(0, 255) for _ in range(8)]
        moving = random.choice([True, False])
        times = [0.0]
        process_emg(emg, moving, times)
        root.after(5, random_emg)

    def random_imu():
        quat = [random.rand]
        acc = []
        gyro = []

    frame = Frame(root, width=100, height=100)
    frame.bind("<KeyPress>", keydown)
    frame.bind("<KeyRelease>", keyup)
    frame.pack()
    frame.focus_set()

    if args.no_myo:
        root.after(1000, random_emg)

    root.mainloop()

    # Enable repeat trigger of keypress events
    os.system('xset r on')


if __name__ == "__main__":
    main()
