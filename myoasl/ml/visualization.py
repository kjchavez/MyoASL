import matplotlib.pyplot as plt
import argparse
import numpy as np

from myoasl.ml.preprocess import *

STYLES = ['r','g','b','c']

def plot_all(data, labels):
    plt.figure()
    input_dim = data[0].shape[1]
    rows = int(np.ceil(np.sqrt(input_dim)))
    cols = (input_dim + rows - 1) / rows

    for i in xrange(len(data)):
        for j in xrange(input_dim):
            plt.subplot(rows, cols, j)
            style = STYLES[labels[i] % len(STYLES)]
            plt.plot(data[i][:, j], style)

    plt.xlabel("time")
    plt.ylabel("")
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')

    args = parser.parse_args()

    data, labels = load_time_series(args.data_file)

    plot_all(data, labels)

if __name__ == "__main__":
    main()
