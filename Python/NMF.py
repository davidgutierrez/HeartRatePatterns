# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 00:50:49 2017
Utils for calculating the NMF
@author: David Gutierrez
"""
from sklearn.decomposition import NMF
from sklearn.model_selection import train_test_split


import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath("/home/scidb/HeartRatePatterns/Python"))
from LogisticRegresion import ajustLogisticRegression

def generateNMF(patients, survived, n_components=30):
    """Generates a NMF and gives a Logistic Regression trained,
    the model, the table actor, the roc_auc and accurracy of the
    Logistic Regresion.
    Keyword arguments:
    patients -- matrix with the heartbeats of the patients
    survived -- list that indicates thet the row of patient survived
    n_components -- number of components of the table
    """
    nmf = NMF(n_components=n_components, random_state=0, alpha=.1, l1_ratio=0)
    patients_nmf = nmf.fit_transform(patients) 
    m_train, m_test, l_train, l_test = train_test_split(patients_nmf,
                                                        survived,
                                                        test_size=0.2,
                                                        random_state=42)
    result = ajustLogisticRegression(m_train, l_train, m_test, l_test)
    predict_poba = result['model'].predict_proba(m_train)[:, 1]
    result.update({'patients_test':m_test, 'nmf':nmf,
    'patients_nmf':patients_nmf, 'predict_poba':predict_poba,
    'survived_test':l_train})
    return result

#from operator import itemgetter
from scipy.stats.stats import pearsonr
def find_pearson(value, patient, survived):
#    pearsonList = []
    result = -100
    for i in range(value):
        patientpear = patient[:, i]
        pearson = pearsonr(patientpear, survived)
        if pearson[0] > result:
            result = pearson[0]
#        pearsonList.append({'group':i,'p1':pearson[0],'p2':pearson[1]})
#    sortedList = sorted(pearsonList, key=itemgetter('p1'), reverse=True)
    return result

def plot_pearson(title,pearson):
    leng = range(1, len(pearson)+1)
    maxperson = max(pearson)
    indxperson = pearson.index(maxperson)
    plt.subplot(111)
    plt.plot(leng, pearson, lw=2)
    plt.annotate('maximo ('+str(maxperson)+","+str(indxperson+2)+")",
                 xy=(indxperson, maxperson),
                 xytext=(indxperson+5, maxperson-0.02),
                 arrowprops=dict(facecolor='black', shrink=0.15))
    plt.xlim([1, 100])
    plt.title(title)
    plt.xlabel('Valor de k en NMF')
    plt.show()

def plot_error(title, pearson):
    leng = range(2, len(pearson)+2)
    plt.subplot(111)
    plt.plot(leng, pearson, lw=2)
    plt.title(title)
    plt.xlabel('Valor de k en NMF')
    plt.show()

def find_best_NMF(patients, survived):
    fig_size = [16, 4]
    plt.rcParams["figure.figsize"] = fig_size
    result = []
    old_err = None
    for value in range(2, 100):
        print(value,end=",")
        diction = generateNMF(patients, survived, n_components=value)
        err_new = diction['nmf'].reconstruction_err_
        diff_err = None if old_err is None else old_err-err_new
        old_err = err_new
#        diction.update({'n_components':value})
        result.append({'pearson':find_pearson(value, diction['patients_nmf'], survived),
                       'recostrucción error': err_new,
                       'diffErr':diff_err,
                       'accuracy':diction['accuracy'],
                       'roc_auc':diction['roc_auc']})
    plot_pearson('pearson',[d['pearson'] for d in result])
    plot_error('recostrucción error',
              [d['recostrucción error'] for d in result])
    plot_error('diferencia del Error', [d['diffErr'] for d in result])
    plot_pearson('Presición', [d['accuracy'] for d in result])
    plot_pearson('Area bajo la curva', [d['roc_auc'] for d in result])
