# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:31:42 2017

@author: quaner
"""

# import breast_preprocessed.spydata

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression

# First step: use mutual information to reduce the dimension
mi = mutual_info_regression(breast_train_scaled.iloc[0:78,:], label_train)
mi /= np.max(mi)

breast_train_scaled_1 = breast_train_scaled.iloc[:, mi > 0.3] # 0.3 is a threshold ,the rest features are 1744
