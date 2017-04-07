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
breast_train = pd.DataFrame(breast_train,index=range(1,79),columns=range(1,24482))
label_train = pd.DataFrame(label_train)
breast_test = pd.DataFrame(breast_test,index=range(1,20),columns=range(1,24482))
label_test = pd.DataFrame(label_test)

# 归一化
from sklearn import preprocessing


(breast_train-breast_train.mean)/breast_train.std > 3




breast_train = preprocessing.normalize(breast_train.T)
breast_train = breast_train.T
breast_test = preprocessing.normalize(breast_test.T)
breast_test = breast_test.T


 