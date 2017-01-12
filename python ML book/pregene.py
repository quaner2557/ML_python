import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# io read the data
datatrainall = pd.read_csv(r'C:\Users\jiang\Desktop\dataset\traindata.csv',header = 0)
datatestall = pd.read_csv(r'C:\Users\jiang\Desktop\dataset\testdata.csv',header = 0)

# delete the first column
datatrain = datatrainall.drop('Gene Accession Number',axis = 1)
datatest = datatestall.drop('Gene Accession Number',axis = 1)

# standard the data
datatrain[datatrain < 100] = 100
datatest[datatest < 100] =100
datatrain[datatrain >16000] = 16000
datatest[datatest > 16000] =16000

# delete some features
max_train = datatrain.max()
min_train = datatrain.min()
for i in range(7129):
    if max_train[i]/min_train[i] < 5:
        datatrain.iloc[:,i] = None
    elif max_train[i] - min_train[i] < 500 :
        datatrain.iloc[:,i] = None

# delete nan
datatrain_full = datatrain.dropna(axis = 1, how='any')

# log10
datatrain = np.log10(datatrain_full)