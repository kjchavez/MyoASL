"""Preprocessing utilties
"""
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

def fit_to_window(signal,window):
    return scipy.signal.resample(signal,window)

def plot_signal(signal,dt,fig=None):
    if not fig:
        fig = plt.figure()
    t = np.arange(signal.shape[0])*dt
    fig.plot(t, signal)


# My use case
dt = 5e-3 # 5 milliseconds
nx = 300
tx = np.arange(nx)*dt
x = np.sin(2*np.pi*tx)

ny = 200
ty = np.arange(ny)*dt
y = scipy.signal.resample(x,ny)
plt.plot(tx,x)
plt.plot(ty,y)
plt.show()
