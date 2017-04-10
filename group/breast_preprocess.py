# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:32:24 2017

@author: quaner
"""

import scipy.io as scio

# 读取数据
breast_train = scio.loadmat('E:/data/breastcancer/breast_train.mat')
breast_test = scio.loadmat('E:/data/breastcancer/breast_test.mat')
label_train = scio.loadmat('E:/data/breastcancer/label_train.mat')
label_test = scio.loadmat('E:/data/breastcancer/label_test.mat')

breast_train = breast_train['breast_train']
breast_test =breast_test['breast_test']
label_train = label_train['label_train']
label_test = label_test['label_test']


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 转化为pandas数据类型
breast_train = pd.DataFrame(breast_train)
label_train = pd.DataFrame(label_train)
breast_test = pd.DataFrame(breast_test)
label_test = pd.DataFrame(label_test)


# 修改outlier并归一化
from sklearn import preprocessing

for i in range(78):
    for j in range(24481):
        if breast_train.iloc[i,j] > 2:
            breast_train.iloc[i,j] = 2

for i in range(19):
    for j in range(24481):
        if breast_test.iloc[i,j] > 2:
            breast_test.iloc[i,j] = 2

breast_train_scaled = preprocessing.scale(breast_train) #  scale处理之后为零均值和单位方差
breast_test_scaled = preprocessing.scale(breast_test)
breast_train_scaled = pd.DataFrame(breast_train_scaled)
breast_test_scaled = pd.DataFrame(breast_test_scaled)

index = pd.DataFrame(np.arange(1,24481))                #加上特征号索引
breast_train_scaled = pd.concat([breast_train_scaled,index.T])
breast_test_scaled = pd.concat([breast_test_scaled,index.T])



 