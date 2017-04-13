# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 14:48:32 2017

@author: quaner
"""

# import breast_preprocessed_MIfilterd.spydata

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression

np.random.seed(0)
# get the mutual information within features
MI_ff =np.zeros((500,500))
for i in range(500):
    for j in np.arange(i,500):
        MI_ff[i,j] = mutual_info_regression((breast_train_scaled_1.iloc[0:78,i]).reshape((78,1)),(breast_train_scaled_1.iloc[0:78,j]).reshape((78,1)))  
        if i % 10 ==0:
           print(i)

for i in range(499):
    for j in np.arange(i,500):
        MI_ff[j,i] = MI_ff[i,j]


# get the mutual information between features and label        
MI_fl = mutual_info_regression(breast_train_scaled_1.iloc[0:78,:], label_train)

# the best 50 features
candidate = np.zeros((500,1))     # 对应位置为1表示属于best 50
for i in range(50):
    if i == 0:
        k = (np.where(MI_fl == np.max(MI_fl)))[0]
        candidate[k] = 1       
    else:
        mrmr = np.zeros((500,1))
        for j in range(500):
            mrmr[j] = (1-candidate[j])*(MI_fl[j]/i-np.sum(np.dot(MI_ff[j,:],candidate)/i**2))-1000*candidate[j]   # 1000*candidate[j]惩罚项
        k = (np.where(mrmr == np.max(mrmr,axis=1)))[0]
        candidate[k] = 1

