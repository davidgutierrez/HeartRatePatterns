# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 01:06:25 2017
Methods used in the matrix
@author: David Gutierrez
"""
import psycopg2
import pandas as pd
import numpy as np


def select_matrix(with_pearson, dbname="mimic"):
    """Selects the current state of the matrix.
    """
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    select_stament = '''SELECT m.subject_id,m.word,m.counting,s.isalive
    FROM matrix m LEFT JOIN subjectwords s ON m.subject_id=s.subject_id'''
    # WHERE m.word in (select word FROM wordspearson WHERE
    # p1>0.01 order by p1 desc limit 400) "
    if with_pearson:
        select_stament = select_stament+''' WHERE m.word in (SELECT word FROM
        wordspearson order by p1 desc limit 400)'''
    cur.execute(select_stament)
    select = []
    for row in cur:
        select.append((row))
    cur.close()
    conn.close()
    return select

def convert_matrix(with_pearson=False, sumvals=True):
    """Selects the current state of the matrix.
    """
    labels = ['subject_id', 'Word', 'Counting', 'isAlive']
    dataframe = pd.DataFrame.from_records(select_matrix(with_pearson),
                                          columns=labels)
    print(len(dataframe))
    table = pd.pivot_table(dataframe, index=["subject_id", "isAlive"],
                           columns=["Word"], values=["Counting"],
                           aggfunc={"Counting":
                               [np.sum if sumvals else np.count_nonzero]},
                           fill_value=0)
    table.columns = [value[2] for value in table.columns.values]
    return table
