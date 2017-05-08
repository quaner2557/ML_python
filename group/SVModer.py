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

import os
os.chdir("/media/quan/软件/AAAAA/ML_python/group")
import APSOmodule
from imp import reload
reload(APSOmodule) 
f=open('f.txt','w')
for times in range(5):
   [gbestpos,gbestval,gbestvals,iterbestvals,pbestpos,pos] = APSOmodule.HAPSO3(50,data,50,10,2000,label_train)
   for gene in range(50):
       if gbestpos[gene] == 1:
          f.write(str(gene)+'\n')
   f.write(str(gbestval)+'\n')
f.close()


from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import pandas as pd
from sklearn.metrics import accuracy_score

ind = [376,373,10667]
testdata = breast_test_scaled.iloc[:19,ind]
traindata = breast_train_scaled.iloc[:78,ind]
C_range = np.logspace(-2, 2, 10)
gamma_range = np.logspace(-2, 2, 10)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
grid.fit(traindata, label_train)
clf =  SVC()
clf.fit(traindata, label_train)
y_pred = grid.predict(testdata)
y_pred2 = clf.predict(testdata)
print(accuracy_score(label_test, y_pred))
