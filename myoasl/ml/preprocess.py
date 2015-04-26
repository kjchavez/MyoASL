import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import sys

from sklearn.cross_validation import train_test_split

INPUT_DIM = 8 # Defined by Myo API
IMU_DIM = 10 # 4 for Quat, 3 for acceleration, 3 for gyro

def load_time_series(filename):
    """Returns a list of numpy arrays and a numpy array of labels. """
    labels = []
    data = []
    imu_data = []

    with open(filename) as fp:
        for line in fp:
            label, emg, imu = line.split('\t', 2)
            labels.append(int(label))
            emg = np.fromstring(emg, dtype=np.uint8, sep=',')
            emg = emg.reshape(-1, INPUT_DIM)
            data.append(emg)
            
            imu = np.fromstring(imu, dtype=int, sep=',')
            imu = imu.reshape(-1, IMU_DIM)
            imu_data.append(imu)

    return data, imu_data, np.array(labels, dtype=int)


def to_fixed_length(data, series_length, dimension):
    """Converts list of arbitrary length np arrays to 2D array of fixed length.

    Args:
        data: list of 2D array-like objects of arbitrary length
        series_length: desired length for all arrays in data

    Returns:
        A len(data) by series_length numpy array of floats obtained by
        'stretching' or 'compressing' the original time series as necessary.
    """
    assert len(data) > 0

    # Note, even though the original data is typically unsigned ints,
    # the resampling may introduce non-integer data points.
    fixed_length_data = np.empty((len(data), series_length*dimension), dtype=float)
    for i, series in enumerate(data):
        fixed_length_series = scipy.signal.resample(series, series_length)
        fixed_length_data[i, :] = fixed_length_series.ravel()

    return fixed_length_data

def merge_data(emg_data, imu_data, series_length=200):
    emg_data = to_fixed_length(emg_data, series_length, INPUT_DIM)
    imu_data = to_fixed_length(imu_data, series_length, IMU_DIM)

    # n x datapoint x datapoint_dim
    emg_data = emg_data.reshape((emg_data.shape[0], -1, INPUT_DIM))
    imu_data = imu_data.reshape((imu_data.shape[0], -1, IMU_DIM))[:,:,0:4] / 100.0

    X = np.concatenate((emg_data, imu_data), axis=2)
    X = X.reshape(emg_data.shape[0], -1)

    return X

def create_train_val_splits(filename, series_length=200, test_size=0.3):
    emg_data, imu_data, labels = load_time_series(filename)

    X = merge_data(emg_data, imu_data, series_length=series_length)
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

def test_data_reading():
    x_train, x_val, y_train, y_val = create_train_val_splits(sys.argv[1])
    print np.bincount(y_train)
    print np.bincount(y_val)

if __name__ == "__main__":
    test_data_reading()
