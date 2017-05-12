# -*- coding: utf-8 -*-
"""
use mrmr filter to select features
data is the D1*D2 dimensional data
num is the number of features we want to save

@author: quaner
"""

# import breast_preprocessed_MIfilterd.spydata
def mrmrfilter(data,label,num):
    import numpy as np
    import pandas as pd
    from sklearn.feature_selection import mutual_info_regression

    np.random.seed(0)
    D1 = data.shape[0]
    D2 = data.shape[1]
    # get the mutual information within features
    MI_ff =np.zeros((D2,D2))
    for i in range(D2):
        print('complete {} part of lines' .format(i/D2) )
        for j in np.arange(i,D2):
            MI_ff[i,j] = mutual_info_regression(data.values[:,i].reshape(D1,1),data.values[:,j].reshape(D1,1), n_neighbors=5)  


    for i in range(D2-1):
        for j in np.arange(i,D2):
            MI_ff[j,i] = MI_ff[i,j]


    # get the mutual information between features and label        
    MI_fl = mutual_info_regression(data.values[:,:].reshape(D1,D2), label.values[:,0].reshape(D1,1), n_neighbors=5)

    # the best 50 features
    candidate = np.zeros((D2,1))     # 对应位置为1表示属于best 50
    for i in range(num):
        if i == 0:
            k = (np.where(MI_fl == np.max(MI_fl)))[0]
            candidate[k] = 1       
        else:
            mrmr = np.zeros((D2,1))
            for j in range(D2):
                mrmr[j] = (1-candidate[j])*(MI_fl[j]/i-np.sum(np.dot(MI_ff[j,:],candidate)/i**2))-1000*candidate[j]   # 1000*candidate[j]惩罚项
            k = (np.where(mrmr == np.max(mrmr,axis=0)))[0]
            candidate[k] = 1

    data_num = np.zeros((D1,num))
    count = 0
    for i in range(D2):
        if candidate[i] == 1:
            data_num[:,count] = data.iloc[:,i]
            count += 1

    return data_num


