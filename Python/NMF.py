# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 00:50:49 2017
Utils for calculating the NMF
@author: David Gutierrez
"""
from sklearn.decomposition import NMF
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

import sys
import os
sys.path.append(os.path.abspath("/home/scidb/HeartRatePatterns/Python"))
from LogisticRegresion import ajustLogisticRegression

def auc_model(name, model, patients, survived):
    """Calculates the roc_auc of a logistic regression
    Keyword arguments:
    name -- name of the Model
    model -- logistic regression trained
    patients -- matrix with the heartbeats of the patients
    survived -- list that indicates thet the row of patient survived
    """
    logit_roc_auc = roc_auc_score(survived, model.predict(patients))
    print(name+" AUC = %2.3f2f"% logit_roc_auc)
    return logit_roc_auc

def generateNMF(patients, survived, n_components=30):
    """Generates a NMF and gives a Logistic Regression trained,
    the model, the table PatientsXFactor, the roc_auc and accurracy of the
    Logistic Regresion.
    Keyword arguments:
    patients -- matrix with the heartbeats of the patients
    survived -- list that indicates thet the row of patient survived
    n_components -- number of components of the table
    """
    nmf = NMF(n_components=n_components, random_state=1, alpha=.1, l1_ratio=.5)
    patients_nmf = nmf.fit_transform(patients)
    m_train, m_test, l_train, l_test = train_test_split(patients_nmf,
                                                        survived,
                                                        test_size=0.2,
                                                        random_state=42)
    model, acurracy = ajustLogisticRegression(m_train, l_train, m_test, l_test)
    name = "NMF "+str(n_components)
    nmf_roc_auc = auc_model(name, model, m_test, l_test)
    return model, nmf, patients_nmf, nmf_roc_auc, acurracy

#from operator import itemgetter
from scipy.stats.stats import pearsonr
def find_pearson(value, patient, survived):
#    pearsonList = []
    p1 = -100
    for i in range(value):
        patientpear = patient[:, i]
        pearson = pearsonr(patientpear, survived)
        if pearson[0] > p1:
            p1 = pearson[0]
#        pearsonList.append({'group':i,'p1':pearson[0],'p2':pearson[1]})
#    sortedList = sorted(pearsonList, key=itemgetter('p1'), reverse=True)
    return p1

def find_best_NMF(patients, survived):
    p1 = 0
    for value in range(2, 100):
        modelNew, nmfNew, patientNew, newrc, acc = generateNMF(patients,
                                                            survived,
                                                            n_components=value)
        maxp1 = find_pearson(value, patientNew, survived)
        print("pearson", maxp1)
        if maxp1 > p1:
            model, nmf, patient = modelNew, nmfNew, patientNew
            roc_auc, accuracy = newrc, acc
            p1, score = maxp1, value
    return model, nmf, patient, roc_auc, accuracy, p1, score
