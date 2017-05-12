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
for times in range(10):
    print(times)
    [gbestpos,gbestval,gbestvals,iterbestvals,pbestpos,pos] = APSOmodule.HAPSO3(50,data,50,10,500,label_train)
    ind1 = []
    ind2 = []
    for gene in range(50):
        if gbestpos[gene] == 1:
            ind1.append(gene)
            ind2.append(breast_train_50_oder[78,gene]-1)
        testdata = breast_test_scaled.iloc[:19,ind2]
        traindata = breast_train_scaled.iloc[:78,ind2]
        clf =  SVC()
        clf.fit(traindata, label_train)
        y_pred = clf.predict(traindata)
        y_pred2 = clf.predict(testdata)
    f.write(str(accuracy_score(label_train, y_pred))+'  '+str(accuracy_score(label_test, y_pred2))+' ')
    f.write(str(ind1)+' ')
    f.write(str(ind2)+' ')
    f.write(str(gbestval)+'\n')    
f.close()


from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import pandas as pd
from sklearn.metrics import accuracy_score

f=open('ff.txt','w')
for i in range(50):
    for j in np.arange(i,50):
        for k in np.arange(j,50):
            ind = [breast_train_50_oder[78,i]-1,breast_train_50_oder[78,j]-1,breast_train_50_oder[78,k]-1]
            testdata = breast_test_scaled.iloc[:19,ind]
            traindata = breast_train_scaled.iloc[:78,ind]
            clf =  SVC()
            clf.fit(traindata, label_train)
            y_pred = clf.predict(traindata)
            y_pred2 = clf.predict(testdata)
            f.write(str(accuracy_score(label_train, y_pred))+'  '+str(accuracy_score(label_test, y_pred2))+'\n')   
    print(i)       
f.close()
datatestt = pd.read_table('ff.txt',header=None,delim_whitespace=True)   
datatestt.columns = ['A','B']
aaa = datatestt.sort(columns='A')        
import matplotlib.pyplot as plt
plt.plot(aaa.iloc[:,0],aaa.iloc[:,1], 'ro')
            
ind = [12258.0, 376.0, 20506.0, 15925.0]
testdata = breast_test_scaled.iloc[:19,ind]
traindata = breast_train_scaled.iloc[:78,ind]
C_range = np.logspace(-2, 2, 10)
gamma_range = np.logspace(-2, 2, 10)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
grid.fit(traindata, label_train)
y_pred = grid.predict(testdata)
print(accuracy_score(label_test, y_pred))

for i in np.arange(0.01,2,0.1):
        clf =  SVC(C=i)
        clf.fit(traindata, label_train)
        y_pred2 = clf.predict(testdata)
        print(accuracy_score(label_test, y_pred2))



