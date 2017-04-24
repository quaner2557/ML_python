# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:51:49 2017

@author: quaner
"""

def HAPSO(ps,data,features,div,Maxiters,label_train):
    from sklearn.model_selection import StratifiedShuffleSplit
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    import numpy as np
    import pandas as pd
    import random
    import math
    F=1                                  # 摄动因子最大值
    F_MIN=0.5                            # 摄动因子最小值
    F_DEC=(F-F_MIN)/Maxiters             # 摄动因子减小量
    gbestvals = {}                       # 用于保存最优值
    fp = {}                              # 用于保存进化因子
    C_range = np.logspace(-1, 3, 5)
    gamma_range = np.logspace(-2, 2, 5)
    param_grid = dict(gamma=gamma_range, C=C_range)
    """
       初始化，根据权重分组选取
       速度区间为[-2,2]
    """
    pos = np.zeros((ps,features)) # 这里ps=features=50，否则有点问题
    for i in range(ps):
        k = math.ceil((i+1)/div)   # 每组div个features，向上取整确定是第几组
        for j in range(k*div):
            if np.random.rand(1)>0.5:
                pos[i,j] = 1

    vel = (2 - -2) * np.random.random_sample((ps,features)) + -2   # 随机产生速度
    out = np.zeros((ps,1))
    for i in range(ps):
        ind = []
        for a,b in enumerate(pos[i,:]):
            if b>0:
                ind.append(a)
        traindata = data[:,ind]
        cv = StratifiedShuffleSplit(test_size=0.2, random_state=40)
        grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
        grid.fit(traindata, label_train)
        out[i] = grid.best_score_/(1+0.01*len(ind))

    pbestpos = pos
    pbestval = out
    gbestval = np.max(pbestval)
    idMax = np.argmax(pbestval)
    gbestpos = pbestpos[idMax,:]
    gbestvals[1] = gbestval
    fp[1]=123.456

    inertiaV=0.9                             # 初始化，惯性系数
    CurrentState=1                           # 初始化，当前状态
    ac1 = 2                                    # 初始化，加速度系数2，认知项
    ac2 = 2                                    # 初始化，加速度系数2，社会项

    LastState=CurrentState
    """
     循环体，更新速度和位置
     更新个体最优位置及适应值，整体最优位置及适应值
     惯性系数，加速度系数，进化因子及进化状态
    """
    for iters in range(Maxiters):
         print(iters)
         rannum1 = np.random.rand(ps,features)
         rannum2 = np.random.rand(ps,features)
         ac11 = rannum1*ac1
         ac22 = rannum2*ac2
         vel = inertiaV*vel + ac11*(pbestpos-pos) +ac22*(np.tile(gbestpos,(ps,1))-pos)
         for t in range(ps):
             for p in range(features):
                 if 1 / (1 + math.exp(-vel[t,p])) >=0.5:
                     pos[t,p] = 1
                 else:
                     pos[t,p] = 0

         tempout = np.zeros((ps, 1))
         for q in range(ps):    # 计算新的pbestpos,pbestval,gbest,gbestvals
             ind = []
             for a,b in enumerate(pos[q,:]):
                 if b>0:
                     ind.append(a)
             traindata = data[:,ind]
             cv = StratifiedShuffleSplit(test_size=0.2, random_state=40)
             grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
             grid.fit(traindata, label_train)
             tempout[q] = grid.best_score_/(1+0.01*len(ind))
             if tempout[q] > pbestval[q]:
                 pbestval[q] = tempout[q]
                 pbestpos[q,:] = pos[q,:]
              
         gbestval = np.max(pbestval)
         idMax = np.argmax(pbestval)
         gbestpos = pbestpos[idMax,:]
         gbestvals[iters+2] = gbestval
          
         EvoFac=getEvoFactor(pos,idMax)               #进化因子
         CurrentState=getState(EvoFac,LastState)      #当前状态
         
         F=F-F_DEC
         if CurrentState==3:
            LastState=CurrentState
            tempPos=gbestpos   
            # 变异                 
            dimchange = np.random.randint(0.1*features)                 
            change = random.sample(range(features),dimchange)                   
            tempPos[change] = 1 - tempPos[change]                  
            ind = []
            for a,b in enumerate(tempPos):
                 if b>0:
                     ind.append(a)
            traindata = data[:,ind]
            cv = StratifiedShuffleSplit(test_size=0.2, random_state=40)
            grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
            grid.fit(traindata, label_train)
            tempPosval = grid.best_score_/(1+0.01*len(ind))
             
            if tempPosval > gbestval:
                 gbestval=tempPosval
                 gbestpos=tempPos             
                 pos[idMax,:]=gbestpos
                    
         EvoFac=getEvoFactor(pos,idMax)
         fp[iters+2]=EvoFac
         inertiaV=1/(1+1.5*math.exp(-2.6*EvoFac))
         CurrentState=getState(EvoFac,LastState)
         [ac1,ac2]=getAc(CurrentState,ac1,ac2)
         LastState=CurrentState

    return gbestpos,gbestval,gbestvals


def getAc(CurrentState,ac1,ac2):

  coe1=0.02
  coe2=0.01
  if CurrentState==1 or CurrentState==4:
      ac1=ac1+(2.2-ac1)*coe1
  else:
      ac1 = ac1+(2-ac1)*coe2

  ac2 = 4-ac1

  return ac1,ac2

def getState(EvoFac,LastState):

  if LastState == 1:
      if EvoFac<=0.2:
          CurrentState = 3
      elif EvoFac<=0.5:
          CurrentState = 2
      elif EvoFac<0.8:
          CurrentState = 1
      else:
          CurrentState = 4

  elif LastState == 2:
    if EvoFac<=0.233:
        CurrentState = 3
    elif EvoFac<0.6:
        CurrentState = 2
    elif EvoFac<=0.7:
        CurrentState = 1
    else:
        CurrentState = 4

  elif LastState == 3:
    if EvoFac<=0.3:
        CurrentState = 3
    elif EvoFac<=0.4:
        CurrentState = 2
    elif EvoFac<0.7:
        CurrentState = 1
    else:
        CurrentState = 4

  else:
    if EvoFac<=0.2:
        CurrentState = 3
    elif EvoFac<=0.4:
        CurrentState = 2
    elif EvoFac<0.767:
        CurrentState = 1
    else:
        CurrentState = 4

  return CurrentState

def getEvoFactor(pos,idgbest):
   import numpy as np
   import math
   ps=pos.shape[0]
   AveDistances=np.zeros((ps,1))
   for i in range(ps):
       t=np.tile(pos[i,:],(ps,1))-pos
       squa = np.sum(t*t,1)
       AveDistances[i]=np.sum([math.sqrt(squ) for squ in squa])/(ps-1)

   Dmax=max(AveDistances)
   Dmin=min(AveDistances)
   Dgbest=AveDistances[idgbest]
   EvoFac=(Dgbest-Dmin)/(Dmax-Dmin)
   return  EvoFac
