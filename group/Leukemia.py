from scipy.io import arff
import os
import pandas as pd
os.chdir('D:\AAAAA\ML_python\group')
data, metadata = arff.loadarff('dataset\Leukemia.arff')
data = pd.DataFrame(data)