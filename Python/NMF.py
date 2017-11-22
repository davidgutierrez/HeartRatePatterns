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
    the model, the table PatientsXFactor, the roc_auc and accurracy of the
    Logistic Regresion.
    Keyword arguments:
    patients -- matrix with the heartbeats of the patients
    survived -- list that indicates thet the row of patient survived
    n_components -- number of components of the table
    """
    nmf = NMF(n_components=n_components, random_state=1, alpha=.1, l1_ratio=0)
    patients_nmf = nmf.fit_transform(patients)
    m_train, m_test, l_train, l_test = train_test_split(patients_nmf,
                                                        survived,
                                                        test_size=0.2,
                                                        random_state=42)
    model, acurracy, roc_auc = ajustLogisticRegression(m_train,
                                                      l_train, m_test, l_test)
    return model, nmf, patients_nmf, acurracy, roc_auc

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

def plotPearson(pearson):
    leng = range(1, len(pearson)+1)
    maxperson = max(pearson)
    indxperson = pearson.index(maxperson)
    plt.subplot(111)
    plt.plot(leng, pearson, lw=2)
    plt.annotate('maximo ('+str(maxperson)+","+str(indxperson+2)+")",
                 xy=(indxperson, maxperson),
                 xytext=(indxperson+20, maxperson+0.02),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.xlim([1, 100])
#    plt.ylim(0.02, 0.20)
    plt.title('''Punto máximo de Pearson en cada iteración de K
    en la matriz pacientes por conjunto de latidos''')
    plt.xlabel('Valor de k en NMF')
    plt.ylabel('Máximo valor de Pearson')
    plt.show()

def plotError(title, pearson):
    leng = range(2, len(pearson)+2)
    plt.subplot(111)
    plt.plot(leng, pearson, lw=2)
    plt.xlim([1, 100])
    plt.title(title)
#    plt.ylim(0.02, 0.20)
    plt.xlabel('Valor de k en NMF')
    plt.ylabel('Máximo valor de Pearson')
    plt.show()

def find_best_NMF(patients, survived):
    result = []
    oldErr = None
    for value in range(2, 100):
        _, nmf, patient, acc, roc_auc = generateNMF(patients,
                                                            survived,
                                                            n_components=value)
        errNew = nmf.reconstruction_err_
        diffErr = None if oldErr is None else oldErr-errNew
        oldErr = errNew
        diction = {'n_components':value,
        'pearson':find_pearson(value, patient, survived),
                       'recostrucción error': errNew,
                       'accuracy':acc, 'roc_auc':roc_auc,
                       'diffErr':diffErr}
        print(diction)
        result.append(diction)
    plotPearson([d['pearson'] for d in result])
    plotError('recostrucción error',
              [d['recostrucción error'] for d in result])
    plotError('diferencia del Error', [d['diffErr'] for d in result])
    plotError('Presición', [d['accuracy'] for d in result])
    plotError('Area bajo la curva', [d['roc_auc'] for d in result])
