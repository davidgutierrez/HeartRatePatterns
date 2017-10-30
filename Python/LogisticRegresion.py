'''
Created on 10/06/2016
Utils for patient_predict module
@author: Andres Moreno B
'''

import numpy as np
from sklearn.linear_model import LogisticRegressionCV,LogisticRegression
from sklearn.metrics import accuracy_score

def find_new_explore_c(paramArray, best_val):
    index_val = paramArray.index(best_val)
    distance_next = float('inf') if index_val == len(paramArray) - 1 else float(paramArray[index_val + 1] - paramArray[index_val])
    distance_prev = float('inf') if index_val == 0 else float(paramArray[index_val] - paramArray[index_val - 1])
    if index_val!=0 and index_val!=len(paramArray)-1:
        start = paramArray[index_val - 1]+distance_prev/2
        paramArray = np.linspace(start, paramArray[index_val + 1]-distance_next/2, len(paramArray)).tolist()
    else:
        new_range=min(distance_next,distance_prev)
        min_val = 0.0001 if best_val - new_range <= 0 else float(best_val - new_range)
        max_val = float(best_val + new_range)
        if index_val==0:
            paramArray = np.linspace(min_val, paramArray[index_val + 1]-distance_next/2, len(paramArray)).tolist()            
        else:
            paramArray = np.linspace(paramArray[index_val - 1]+distance_prev/2, max_val, len(paramArray)).tolist()
    return paramArray

def ajustLogisticRegression(model_train,objetive_train,model_test,objetive_test,exploreC=[0.0001,0.001,0.01,0.1,1,10]) :
    best_avg=0
    solver='liblinear'
    for i in range(0,5):
        logitmodel=LogisticRegressionCV(exploreC, fit_intercept=True, cv=5,  penalty='l2', 
                                                dual=True,  solver=solver,  n_jobs=-1, verbose=0, 
                                                refit=True, random_state=0,  scoring='roc_auc'#'f1'#,max_iter=102400
						)
        logitmodel.fit(model_train,objetive_train)
        predictions= logitmodel.predict(model_test)
        scores=logitmodel.scores_[1]
        best_val=logitmodel.C_
        best_average = np.average(scores,0)[exploreC.index(best_val)]
#        print("CV averages for values "+str(exploreC)+" are:"+str(np.average(scores,0)))
        print("Best C is "+str(best_val)+" with an average of "+str(best_average))
        if best_avg<best_average :
          bestC = best_val[0]
          best_avg=best_average
        exploreC=find_new_explore_c(exploreC, best_val)
    #return a logisticRegression vased in the best_val and the parameter used
    acscore = accuracy_score(objetive_test,logitmodel.predict(model_test))
    print("Score logit "+str(acscore))

    model = LogisticRegression(C=best_val[0],fit_intercept=True, penalty='l2',dual=True,solver=solver,verbose=0,random_state=0)
    model.fit(model_train,objetive_train)
    acscoreb = accuracy_score(objetive_test,model.predict(model_test))
    print("Score last "+str(acscoreb))
    acscore = acscoreb if acscoreb>acscore else acscore
    model = model if acscoreb>acscore else logitmodel

    modelC = LogisticRegression(C=bestC      ,fit_intercept=True, penalty='l2',dual=True,solver=solver,verbose=0,random_state=0)
    modelC.fit(model_train,objetive_train)
    acscorec = accuracy_score(objetive_test,modelC.predict(model_test))
    print("Score best "+str(acscorec))
    acscore = acscore if acscore>acscorec else acscorec
    model = modelC if acscorec>acscoreb else model
    print("acurracy is %2.2f" % acscore)
    return model
