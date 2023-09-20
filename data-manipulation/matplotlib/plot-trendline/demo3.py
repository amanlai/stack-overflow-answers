import matplotlib.pyplot as plt
import numpy as np

x_data, y_data = np.repeat(np.linspace(0, 9, 100)[None,:], 2, axis=0) + np.random.rand(2, 100)*2

x_mean, y_mean = np.mean(x_data), np.mean(y_data)
beta = np.sum((x_data - x_mean) * (y_data - y_mean)) / np.sum((x_data - x_mean)**2)
alpha = y_mean - beta * x_mean
y_hat = alpha + beta * x_data

plt.plot(x_data, y_data, 'bo', x_data, y_hat, "r-");