# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:45:18 2017

@author: Administrator

main file of breast cancer
"""


"""
# arff文件太大直接宕机
from scipy.io import arff
os.chdir('D:\AAAAA\ML_python\group')
data, metadata = arff.loadarff('dataset\Breast.arff')
data = pd.DataFrame(data)
"""

import pandas as pd
import scipy.io as scio
import random
from sklearn import preprocessing
import numpy as np

import os
os.chdir('D:/AAAAA/ML_python/group')

# 读取数据
breast_train = scio.loadmat('dataset/breast_train.mat')
breast_test = scio.loadmat('dataset/breast_test.mat')
label_train = scio.loadmat('dataset/label_train.mat')
label_test = scio.loadmat('dataset/label_test.mat')

breast_train = breast_train['breast_train']
breast_test =breast_test['breast_test']
label_train = label_train['label_train']
label_test = label_test['label_test']

breast_train = pd.DataFrame(breast_train)
label_train = pd.DataFrame(label_train)
breast_test = pd.DataFrame(breast_test)
label_test = pd.DataFrame(label_test)

data = pd.concat([breast_train,breast_test])
label = pd.concat([label_train,label_test])

#去除奇异点
for i in range(97):
    print(i)
    for j in range(24481):
        if data.iloc[i,j] > 0.5:
            data.iloc[i,j] = 0.5
        elif data.iloc[i,j] < -0.5:
            data.iloc[i,j] = -0.5

data_scaled = preprocessing.scale(data)
data_scaled = pd.DataFrame(data_scaled,columns=range(24481))

# 将数据分成五等分
groupoder = random.sample(range(97),97)
index1 = groupoder[0:20]
index2 = groupoder[20:40]
index3 = groupoder[40:59]
index4 = groupoder[59:78]
index5 = groupoder[78:97]

test1 = data_scaled.iloc[index1,:]
train1 = pd.concat([data_scaled.iloc[index2,:],data_scaled.iloc[index3,:],data_scaled.iloc[index4,:],data_scaled.iloc[index5,:]])
test1_label = label.iloc[index1,:]
train1_label = pd.concat([label.iloc[index2,:],label.iloc[index3,:],label.iloc[index4,:],label.iloc[index5,:]])

test2 = data_scaled.iloc[index2,:]
train2 = pd.concat([data_scaled.iloc[index1,:],data_scaled.iloc[index3,:],data_scaled.iloc[index4,:],data_scaled.iloc[index5,:]])
test2_label = label.iloc[index2,:]
train2_label = pd.concat([label.iloc[index1,:],label.iloc[index3,:],label.iloc[index4,:],label.iloc[index5,:]])

test3 = data_scaled.iloc[index3,:]
train3 = pd.concat([data_scaled.iloc[index1,:],data_scaled.iloc[index2,:],data_scaled.iloc[index4,:],data_scaled.iloc[index5,:]])
test3_label = label.iloc[index3,:]
train3_label = pd.concat([label.iloc[index1,:],label.iloc[index2,:],label.iloc[index4,:],label.iloc[index5,:]])

test4 = data_scaled.iloc[index4,:]
train4 = pd.concat([data_scaled.iloc[index1,:],data_scaled.iloc[index2,:],data_scaled.iloc[index3,:],data_scaled.iloc[index5,:]])
test4_label = label.iloc[index4,:]
train4_label = pd.concat([label.iloc[index1,:],label.iloc[index2,:],label.iloc[index3,:],label.iloc[index5,:]])

test5 = data_scaled.iloc[index5,:]
train5 = pd.concat([data_scaled.iloc[index1,:],data_scaled.iloc[index2,:],data_scaled.iloc[index3,:],data_scaled.iloc[index4,:]])
test5_label = label.iloc[index5,:]
train5_label = pd.concat([label.iloc[index1,:],label.iloc[index2,:],label.iloc[index3,:],label.iloc[index4,:]])

"""
import 5fold_breast.spydata to replace up file
"""

from imp import reload

# 先通过MI方法去除大部分特征，设置的threshold尽量使特征保持在1000左右
import filtermodule
reload(filtermodule) 

data_MI1 = filtermodule.MIfilter(train1,train1_label,0.35)
data_MI2 = filtermodule.MIfilter(train2,train2_label,0.35)
data_MI3 = filtermodule.MIfilter(train3,train3_label,0.35)
data_MI4 = filtermodule.MIfilter(train4,train4_label,0.35)
data_MI5 = filtermodule.MIfilter(train5,train5_label,0.35)

# 利用mrmr剩下100个特征左右
import mrmrmodule
reload(mrmrmodule)

data_mrmr1 = mrmrmodule.mrmrfilter(data_MI1,train1_label,100)
data_mrmr2 = mrmrmodule.mrmrfilter(data_MI1,train2_label,100)
data_mrmr3 = mrmrmodule.mrmrfilter(data_MI1,train3_label,100)
data_mrmr4 = mrmrmodule.mrmrfilter(data_MI1,train4_label,100)
data_mrmr5 = mrmrmodule.mrmrfilter(data_MI1,train5_label,100)

# 根据SVM权重对100个特征进行排序得到50个genes 
from sklearn.svm import SVR
from sklearn.feature_selection import RFE

rfe = RFE(estimator=SVR(kernel="linear"), n_features_to_select=50,step=1)

selector1 = rfe.fit(data_mrmr1, train1_label)
selector2 = rfe.fit(data_mrmr2, train2_label)
selector3 = rfe.fit(data_mrmr3, train3_label)
selector4 = rfe.fit(data_mrmr4, train4_label)
selector5 = rfe.fit(data_mrmr5, train5_label)

data_svmrfe1 = selector1.transform(data_mrmr1)
data_svmrfe2 = selector2.transform(data_mrmr2)
data_svmrfe3 = selector3.transform(data_mrmr3)
data_svmrfe4 = selector4.transform(data_mrmr4)
data_svmrfe5 = selector5.transform(data_mrmr5)

import APSOmodule
reload(APSOmodule)

data_svmrfe = [data_svmrfe1,data_svmrfe2,data_svmrfe3,data_svmrfe4,data_svmrfe5]
label_APSO = [train1_label,train2_label,train3_label,train4_label,train5_label] 
f=open('result_breast.txt','w')
for d in range(5):    
    for times in range(3):
        print(d)
        print(times)
        [gbestpos,gbestval,gbestvals,iterbestvals,pbestpos,pos] = APSOmodule.HAPSO3(50,data_svmrfe[d],50,10,2000,label_APSO[d])
        ind =[]
        for gene in range(50):
            if gbestpos[gene] == 1:
                ind.append(gene)
                f.write(str(d)+' '+str(times)+' gbestval is '+str(gbestval)+'\n')
                f.write(str(d)+' '+str(times)+' the choosed genes are '+str(ind)+'\n')
f.close
    
