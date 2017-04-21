# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:03:50 2017

@author: quaner
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

from HAPSODS import HAPSO
[gbestpos,gbestval,gbestvals] = HAPSO(50,data,50,10,1000,label_train)