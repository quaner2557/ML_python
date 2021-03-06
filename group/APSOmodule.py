# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:51:49 2017

@author: quaner
"""

def HAPSO1(ps,data,features,div,Maxiters,label_train):
    from sklearn.model_selection import StratifiedShuffleSplit
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    import numpy as np
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
         rannum1 = np.random.rand(ps,features)
         rannum2 = np.random.rand(ps,features)
         ac11 = rannum1*ac1
         ac22 = rannum2*ac2
         vel = inertiaV*vel + ac11*(pbestpos-pos) +ac22*(np.tile(gbestpos,(ps,1))-pos)
         for t in range(ps):
             count = 0 
             for p in range(features):
                 if 1 / (1 + math.exp(-vel[t,p])) >=random.random():
                     pos[t,p] = 1
                     count += 1
                 else:
                     pos[t,p] = 0
                
                 if count == 0:
                     pos[t,random.sample(range(50),1)] = 1

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





"""
   do not use gridsearch
   do not use gridsearch
   do not use gridsearch
   do not use gridsearch
   do not use gridsearch
"""
def HAPSO2(ps,data,features,div,Maxiters,label_train):
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    import numpy as np
    import random, math
    F=1                                  # 摄动因子最大值
    F_MIN=0.5                            # 摄动因子最小值
    F_DEC=(F-F_MIN)/Maxiters             # 摄动因子减小量
    gbestvals = {}                       # 用于保存最优值
    iterbestvals = {}
    fp = {}                              # 用于保存进化因子

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

    vel = (4 - -4) * np.random.random_sample((ps,features)) + -4  # 随机产生速度
    out = np.zeros((ps,1))
    for i in range(ps):
        ind = []
        for a,b in enumerate(pos[i,:]):
            if b>0:
                ind.append(a)
        traindata = data[:,ind]
        X_train, X_test, y_train, y_test = train_test_split(traindata,label_train, test_size=0.2, random_state=0)
        clf = SVC(kernel='rbf', C=2).fit(X_train, y_train)
        out[i] = clf.score(X_test, y_test)/(1+0.03*len(ind))

    pbestpos = pos.copy()
    pbestval = out.copy()
    gbestval = np.max(pbestval)
    idMax = np.argmax(pbestval)
    gbestpos = pbestpos[idMax,:].copy()
    gbestvals[1] = gbestval
    fp[1]=123.456

    inertiaV=0.9                             # 初始化，惯性系数
    CurrentState=1                           # 初始化，当前状态
    ac1 = 4                                    # 初始化，加速度系数2，认知项
    ac2 = 4                                    # 初始化，加速度系数2，社会项

    LastState=CurrentState
    """
     循环体，更新速度和位置
     更新个体最优位置及适应值，整体最优位置及适应值
     惯性系数，加速度系数，进化因子及进化状态
    """
    for iters in range(Maxiters):
         if iters % 100 == 0:
             print("the best of %d is %f\n" %(iters,gbestval))
         rannum1 = np.random.rand(ps,features)
         rannum2 = np.random.rand(ps,features)
         ac11 = rannum1*ac1
         ac22 = rannum2*ac2
         vel = inertiaV*vel + ac11*(pbestpos-pos) +ac22*(np.tile(gbestpos,(ps,1))-pos)
         for t in range(ps):
             count = 0 
             for p in range(features):
                 if 1 / (1 + math.exp(-vel[t,p])) >=random.random():
                     pos[t,p] = 1
                     count += 1
                 else:
                     pos[t,p] = 0
                
                 if count == 0:
                     pos[t,random.sample(range(50),1)] = 1

         tempout = np.zeros((ps, 1))
         for q in range(ps):    # 计算新的pbestpos,pbestval,gbest,gbestvals
             ind = []
             for a,b in enumerate(pos[q,:]):
                 if b>0:
                     ind.append(a)
             traindata = data[:,ind].copy()
             X_train, X_test, y_train, y_test = train_test_split(traindata,label_train, test_size=0.2, random_state=0)
             clf = SVC(kernel='rbf', C=2).fit(X_train, y_train)
             tempout[q] = clf.score(X_test, y_test)/(1+0.03*len(ind))
             if tempout[q] > pbestval[q]:
                 pbestval[q] = tempout[q]
                 pbestpos[q,:] = pos[q,:]
              
         iterbestvals[iters] = np.max(pbestval)
         idMax = np.argmax(pbestval)
         iterbestpos = pbestpos[idMax,:].copy()
         
         if iterbestvals[iters] >= gbestval:
            gbestval = iterbestvals[iters]
            gbestpos = iterbestpos.copy()
         
         gbestvals[iters+2] = gbestval
          
         EvoFac=getEvoFactor(pos,idMax)               #进化因子
         CurrentState=getState(EvoFac,LastState)      #当前状态
         
         F=F-F_DEC
         if CurrentState==3:
            LastState=CurrentState
            tempPos=gbestpos.copy()   
            # 变异                 
            dimchange = np.random.randint(0.1*features)                 
            change = random.sample(range(features),dimchange)                   
            tempPos[change] = 1 - tempPos[change]                  
            ind = []
            for a,b in enumerate(tempPos):
                 if b>0:
                     ind.append(a)
            traindata = data[:,ind].copy()
            X_train, X_test, y_train, y_test = train_test_split(traindata,label_train, test_size=0.2, random_state=0)
            clf = SVC(kernel='rbf', C=2).fit(X_train, y_train)
            tempPosval =  clf.score(X_test, y_test)/(1+0.03*len(ind))
             
            if tempPosval > gbestval:
                 gbestval=tempPosval
                 gbestpos=tempPos.copy()             
                 pos[idMax,:]=gbestpos.copy()
                    
         EvoFac=getEvoFactor(pos,idMax)
         fp[iters+2]=EvoFac
         inertiaV=1/(1+1.5*math.exp(-2.6*EvoFac))
         CurrentState=getState(EvoFac,LastState)
         [ac1,ac2]=getAc(CurrentState,ac1,ac2)
         LastState=CurrentState

    return gbestpos,gbestval,gbestvals,iterbestvals,pbestpos,pos


"""
HAPSO3 增加了更多的local search来增加更优解的寻找
验证方法修改成k-fold

"""

def HAPSO3(ps,data,features,div,Maxiters,label_train):
    from sklearn.model_selection import cross_val_score
    from sklearn.svm import SVC
    import numpy as np
    import random, math
    F=1                                  # 摄动因子最大值
    F_MIN=0.5                            # 摄动因子最小值
    F_DEC=(F-F_MIN)/Maxiters             # 摄动因子减小量
    gbestvals = {}                       # 用于保存最优值
    iterbestvals = {}
    fp = {}                              # 用于保存进化因子
    label_train = label_train.iloc[:,0]
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

    vel = (4 - -4) * np.random.random_sample((ps,features)) + -4  # 随机产生速度
    out = np.zeros((ps,1))
    for i in range(ps):
        ind = []
        for a,b in enumerate(pos[i,:]):
            if b>0:
                ind.append(a)
        traindata = data[:,ind].copy()
        clf = SVC(kernel='rbf', C=2)
        scores = cross_val_score(clf, traindata,label_train,cv=5)
        out[i] = scores.mean()/(1+0.03*len(ind))

    pbestpos = pos.copy()
    pbestval = out.copy()
    gbestval = np.max(pbestval)
    idMax = np.argmax(pbestval)
    gbestpos = pbestpos[idMax,:].copy()
    gbestvals[1] = gbestval
    fp[1]=123.456

    inertiaV=0.9                             # 初始化，惯性系数
    CurrentState=1                           # 初始化，当前状态
    ac1 = 4                                    # 初始化，加速度系数2，认知项
    ac2 = 4                                    # 初始化，加速度系数2，社会项

    LastState=CurrentState
    """
     循环体，更新速度和位置
     更新个体最优位置及适应值，整体最优位置及适应值
     惯性系数，加速度系数，进化因子及进化状态
    """
    for iters in range(Maxiters):
         if iters % 100 == 0:
             print("the best of %d is %f\n" %(iters,gbestval))
         rannum1 = np.random.rand(ps,features)
         rannum2 = np.random.rand(ps,features)
         ac11 = rannum1*ac1
         ac22 = rannum2*ac2
         vel = inertiaV*vel + ac11*(pbestpos-pos) +ac22*(np.tile(gbestpos,(ps,1))-pos)
         for t in range(ps):
             count = 0 
             for p in range(features):
                 if vel[t,p] > 1.5:
                     vel[t,p] = 1.5
                 elif vel[t,p] < -1.5:
                     vel[t,p] = -1.5
                        
                 if 1 / (1 + math.exp(-vel[t,p])) >=random.random():
                     pos[t,p] = 1
                     count += 1
                 else:
                     pos[t,p] = 0
                
                 if count == 0:
                     pos[t,random.sample(range(50),1)] = 1

         tempout = np.zeros((ps, 1))
         for q in range(ps):    # 计算新的pbestpos,pbestval,gbest,gbestvals
             ind = []
             for a,b in enumerate(pos[q,:]):
                 if b>0:
                     ind.append(a)
             traindata = data[:,ind].copy()
             clf = SVC(kernel='rbf', C=2)
             scores = cross_val_score(clf, traindata, label_train, cv=5)
             tempout[q] = scores.mean()/(1+0.03*len(ind))
             if tempout[q] > pbestval[q]:
                 pbestval[q] = tempout[q]
                 pbestpos[q,:] = pos[q,:]
              
         iterbestvals[iters] = np.max(pbestval)
         idMax = np.argmax(pbestval)
         iterbestpos = pbestpos[idMax,:].copy()
         
         if iterbestvals[iters] >= gbestval:
            gbestval = iterbestvals[iters]
            gbestpos = iterbestpos.copy()
         
         gbestvals[iters+2] = gbestval
          
         EvoFac=getEvoFactor(pos,idMax)               #进化因子
         CurrentState=getState(EvoFac,LastState)      #当前状态
         
         F=F-F_DEC
         if CurrentState==3:
            LastState=CurrentState
            tempPos=gbestpos.copy()   
            # 变异                 
            dimchange = np.random.randint(0.1*features)                 
            change = random.sample(range(features),dimchange)                   
            tempPos[change] = 1 - tempPos[change]                  
            ind = []
            for a,b in enumerate(tempPos):
                 if b>0:
                     ind.append(a)
            traindata = data[:,ind].copy()
            clf = SVC(kernel='rbf', C=2)
            scores = cross_val_score(clf, traindata, label_train, cv=5)
            tempPosval =  scores.mean()/(1+0.03*len(ind))
             
            if tempPosval > gbestval:
                 gbestval=tempPosval
                 gbestpos=tempPos.copy()             
                 pos[idMax,:]=gbestpos.copy()
            # 增加DS算法进行局部搜索
            probMut=0.1+0.2*(1-EvoFac)
            oldpos=pos.copy()
            for s in range(ps):
                if np.random.rand()<probMut:
                    p1=0.3*np.random.rand()
                    p2=0.5*np.random.rand()
                    mapp=generate_map_of_active_individuals(ps,p1,p2)
                    R=1/np.random.gamma(1,0.5)
                    pos[s,:]=pos[s,:] + (R*mapp)*(gbestpos-pos[s,:])
                    pos[s,pos[s,:]<=0.5] = 0
                    pos[s,pos[s,:]>0.5] = 1
                    ind = []
                    for a,b in enumerate(pos[s,:]):
                        if b>0:
                           ind.append(a)
                    traindata = data[:,ind].copy()
                    clf = SVC(kernel='rbf', C=2)
                    scores = cross_val_score(clf, traindata, label_train, cv=5)
                    tempPs =  scores.mean()/(1+0.03*len(ind))  
                    if tempPs > tempout[s]:
                        tempout[s] = tempPs
                    else:
                        pos[s,:] = oldpos[s,:].copy()
          
         EvoFac=getEvoFactor(pos,idMax)
         fp[iters+2]=EvoFac
         inertiaV=1/(1+1.5*math.exp(-2.6*EvoFac))
         CurrentState=getState(EvoFac,LastState)
         [ac1,ac2]=getAc(CurrentState,ac1,ac2)
         LastState=CurrentState

    return gbestpos,gbestval,gbestvals,iterbestvals,pbestpos,pos


"""
选择DS算法激活粒子
"""
def generate_map_of_active_individuals(D,p1,p2):
    
    import numpy as np
    import math
    mapp=np.zeros((1,D))
    if np.random.rand()<np.random.rand():
        if np.random.rand()<p1:
            mapp=np.random.rand(1,D)<np.random.rand()                                  
        else:
            mapp[0,np.random.randint(0,D)]=1
    else:
        mapp[0,np.random.randint(0,D,(1,math.ceil(p2*D)))]=1

    return mapp





