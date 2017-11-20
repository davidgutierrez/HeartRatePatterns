# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 01:06:25 2017
Methods used in the matrix
@author: David Gutierrez
"""
import psycopg2
import pandas as pd
import numpy as np


def __select_matrix(with_pearson, filter_words=None, dbname="mimic"):
    """Selects the current state of the matrix.
    """
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    select_stament = '''SELECT m.subject_id,m.word,m.counting,s.isalive
    FROM matrix m LEFT JOIN subjectwords s ON m.subject_id=s.subject_id '''
    if with_pearson:
        select_stament = select_stament+''' INNER JOIN 
        (SELECT word,p1 FROM wordspearson ORDER BY p1 DESC LIMIT 400) w 
        ON m.word=w.word '''
    if filter_words!=None:
        select_stament = select_stament+''' WHERE m.word in %s '''
    if filter_words!=None:
        cur.execute(select_stament,(filter_words,))
    else:
        cur.execute(select_stament)
    select = []
    for row in cur:
        select.append((row))
    cur.close()
    conn.close()
    return select

def convert_matrix(with_pearson=False, sumvals=True,filter_words=None):
    """Selects the current state of the matrix.
    Keyword arguments:
    wave -- the original wave
    word -- the word that represents the wave
     """
    labels = ['subject_id', 'Word', 'Counting', 'isAlive']
    dataframe = pd.DataFrame.from_records(__select_matrix(with_pearson,filter_words),
                                          columns=labels)
    table = pd.pivot_table(dataframe, index=["subject_id", "isAlive"],
                           columns=["Word"], values=["Counting"],
                           aggfunc={"Counting":
                               [np.sum if sumvals else np.count_nonzero]},
                           fill_value=0)
    table.columns = [value[2] for value in table.columns.values]
    print(table.shape)
    return table
