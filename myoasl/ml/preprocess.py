import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from sklearn.cross_validation import train_test_split

INPUT_DIM = 8 # Defined by Myo API

def load_time_series(filename):
    """Returns a list of numpy arrays and a numpy array of labels. """
    labels = []
    data = []
    with open(filename) as fp:
        for line in fp:
            label, series = line.split('\t', 1)
            labels.append(int(label))
            series = np.fromstring(series, dtype=np.uint8, sep=',')
            series = series.reshape(-1,INPUT_DIM)
            data.append(series)

    return data, np.array(labels, dtype=int)


def to_fixed_length(data,series_length):
    """Converts list of arbitrary length np arrays to 2D array of fixed length.

    Args:
        data: list of array-like objects of arbitrary length
        series_length: desired length for all arrays in data

    Returns:
        A len(data) by series_length numpy array of floats obtained by
        'stretching' or 'compressing' the original time series as necessary.
    """
    assert len(data) > 0

    # Note, even though the original data is typically unsigned ints,
    # the resampling may introduce non-integer data points.
    fixed_length_data = np.empty((len(data), series_length*INPUT_DIM), dtype=float)
    for i, series in enumerate(data):
        fixed_length_series = scipy.signal.resample(series, series_length)
        fixed_length_data[i, :] = fixed_length_series.ravel()

    return fixed_length_data

def create_train_val_splits(filename, series_length=200, test_size=0.3):
    data, labels = load_time_series(filename)

    X = to_fixed_length(data, series_length)
    y = labels

    # Split into training and validation set
    X_train, X_val, y_train, y_val = train_test_split(
                                        X, y, test_size=test_size)
    return X_train, X_val, y_train, y_val

def test():
    def plot_signal(signal,dt,fig=None):
        if not fig:
            fig = plt.figure()
        t = np.arange(signal.shape[0])*dt
        ax = fig.gca()
        ax.plot(t, signal)

    # My use case
    dt = 5e-3  # 5 milliseconds
    nx = 300
    tx = np.arange(nx)*dt
    x = np.sin(2*np.pi*tx)
    x = np.vstack((x, x)).T
    fig = plt.figure()
    plt.plot(tx, x)

    ny = 200
    y = scipy.signal.resample(x, ny)
    plot_signal(y, dt, fig=fig)
    plt.show()

if __name__ == "__main__":
    test()
