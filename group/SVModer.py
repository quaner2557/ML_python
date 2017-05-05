# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:03:50 2017

@author: quaner

import breast_preprocessed_mrmr.spydata
"""

import numpy as np
            
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

import APSOmodule
from imp import reload
reload(APSOmodule) 
[gbestpos,gbestval,gbestvals,iterbestvals,pbestpos,pos] = APSOmodule.HAPSO3(50,data,50,10,3000,label_train)


from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import pandas as pd

ind = [3462,12258]
traindata = breast_train_scaled.iloc[:78,ind]
testdata = breast_test_scaled.iloc[:19,ind]
C_range = np.logspace(-2, 2, 10)
gamma_range = np.logspace(-2, 2, 10)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
grid.fit(traindata, label_train)

print("The best parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))
      
clf = SVC(kernel='rbf', C=2).fit(traindata, label_train)
clf.score(testdata, label_test)
clf.score(traindata, label_train)    
