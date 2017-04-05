# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:32:24 2017

@author: quaner
"""

import scipy.io as scio

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

from sklearn.ensemble import ExtraTreesClassifier
# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=10,
                              random_state=0)

forest.fit(breast_train, label_train)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")


# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(breast_train.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(breast_train.shape[1]), indices)
plt.xlim([-1, breast_train.shape[1]])
plt.show()
