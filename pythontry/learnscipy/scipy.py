import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.cross_validation import train_test_split

#记录程序运行时间
import time
start_time = time.time()

#读入数据
train = pd.read_csv("Digit_Recognizer/train.csv")
tests = pd.read_csv("Digit_Recognizer/test.csv")