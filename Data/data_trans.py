import numpy as np
import scipy.stats as stat
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/jackie/Desktop/TSP/Data/qa194.csv")
data_x = data[['x']]
data_y = data[['y']]

x = []
y = []

for i in range(0, len(data_x)):
    x.append(round(float(data_x.iat[i, 0]), 4))

for i in range(0, len(data_y)):
    y.append(round(float(data_y.iat[i, 0]), 4))

