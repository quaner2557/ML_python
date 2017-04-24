# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:03:50 2017

@author: quaner

import breast_preprocessed_mrmr.spydata
"""

import numpy as np
import pandas as pd
            
# 根据SVM权重进行排序 
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

trainX = breast_train_50[:78,:]
svc = SVC(kernel="linear", C=1)
rfe = RFE(estimator=svc, n_features_to_select=50, step=0.1)
rfe.fit(trainX, label_train)
cof = rfe.estimator_.coef_

oder = np.argsort(-cof)
breast_train_50_oder = np.reshape(breast_train_50[:,oder.T],(79,50))
data = breast_train_50_oder[:78,:]

import HAPSODS
from imp import reload
reload(HAPSODS) 
[gbestpos,gbestval,gbestvals] = HAPSODS.HAPSO(50,data,50,10,50,label_train)