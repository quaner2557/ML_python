# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:31:42 2017

@author: quaner
"""

# import breast_preprocessed.spydata
def MIfilter(data,label,threshold):
   import numpy as np
   import pandas as pd
   from sklearn.feature_selection import mutual_info_regression

   np.random.seed(0)

   # First step: use mutual information to reduce the dimension
   mi = mutual_info_regression(data, label)
   mi /= np.max(mi)                                                                  
   data_MI = data.iloc[:, mi > threshold]
   return data_MI
