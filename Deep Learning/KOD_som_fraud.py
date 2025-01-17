#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:53:38 2020

@author: kieranodonnell
"""
''''This script attempts to find fraudluent credit card applications by detecting outliers.
This is done with self-organising machines'''

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/kieranodonnell/Documents/GitHub/Data Sci/Datasets/Credit_Card_Applications.csv')
X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values

# Scale features

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
X = sc.fit_transform(X)

# Training SOM
from minisom import MiniSom
som = MiniSom(x = 10 , y = 10 ,input_len = 15, sigma = 1.0, learning_rate = 0.5)

# Randomly initialise vector weights
som.random_weights_init(X)
som.train_random(data = X, num_iteration=350)

# Visualize results of interneuron distances
from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()
# Fraudulent transactions appear more white

# Finding the frauds
mappings = som.win_map(X)
frauds = np.concatenate((mappings[(8,4)], mappings[(6,8)]), axis = 0)
frauds = sc.inverse_transform(frauds)