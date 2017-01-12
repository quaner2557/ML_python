import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r'C:\Users\jiang\Desktop\dataset\datagenenew.csv',header=0)
df_test = pd.read_csv(r'C:\Users\jiang\Desktop\dataset\datagenenew_test.csv',header=0)

# first two features
labeltrain = df.iloc[:,0].values
labeltest = df_test.iloc[:,0].values
X = df.iloc[:,1:3].values
Y = df_test.iloc[:,1:3].values

fig = plt.figure(figsize=(18,8))

ax1 = fig.add_subplot(1,2,1)
ax1.scatter(X[:27,0],X[:27,1], color='red', marker = 'o')
ax1.scatter(X[27:39,0],X[27:39,1], color='blue', marker = 'x')

ax2 = fig.add_subplot(1,2,2)
ax2.scatter(Y[:20,0],Y[:20,1], color='red', marker = 'o')
ax2.scatter(Y[20:34,0],Y[20:34,1], color='blue', marker = 'x')

fig2 = plt.figure(figsize=(9,8))
plt.scatter(X[:27,0],X[:27,1], color='red', marker = 'o')
plt.scatter(X[27:39,0],X[27:39,1], color='blue', marker = 'x')
plt.scatter(2.735,3.323,color='green',marker = '*')

plt.show()