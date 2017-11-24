# -*- coding: utf-8 -*-
'''
Created on 13/11/2017
Utils for ploting the words in the ECG
@author: David Gutierrez
'''

import wfdb
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

def create_word(dbname="mimic"):
    """Creates the table word."""
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS word
             (id serial PRIMARY KEY,
            word character varying(255),
            wave real[])''')
    conn.commit()
    cur.close()
    conn.close()

def save_word(wave, word, dbname="mimic"):
    """Saves a word in the database.

    Keyword arguments:
    wave -- the original wave
    word -- the word that represents the wave
    """
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    insert_statement = ('INSERT INTO word(word,wave)'
                      ' VALUES (%s,%s)')
    cur.execute(insert_statement, (word, wave.tolist(), ))
    conn.commit()
    cur.close()
    conn.close()

def clean_word(dbname="mimic"):
    """Cleans the table word.

    Keyword arguments:
    wave -- the original wave
    word -- the word that represents the wave
    """
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    delete_statement = '''DELETE FROM word WHERE wave='{}' '''
    cur.execute(delete_statement)
    conn.commit()
    cur.close()
    conn.close()

def select_word(word, dbname="mimic"):
    """select a wave from the word table.

    Keyword arguments:
    word -- the word that is needed
    """
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    insert_statement = 'SELECT wave FROM word WHERE word=%s'
    cur.execute(insert_statement, (word, ))
#    print(cur.mogrify(insert_statement, (word, )))
    result = None
    for wave in cur:
        result = wave[0]
    cur.close()
    conn.close()
    return result

def download_word(wave):
    """downloads the word, after searching it in the mimic data base.
    word -- the word that represents the wave
    """
    print(wave['word'], wave['from'], wave['to'], wave['record'])
    onda = wave['record'].split("/")[3]
    pbdir = wave['record'].replace("/"+onda, '')
    if 'mimic3wdb' in wave['record']:
        pbdir = onda.split("-")[0].replace("s", '').zfill(6)
        onda = onda.replace(onda.split("-")[0].replace("s", ''), pbdir)
        pbdir = (wave['record'].split("/")[0]+'/'+wave['record'].split("/")[1]+
        '/p'+pbdir[:2]+'/p'+pbdir+'/')
        onda = onda.replace('s', 'p')
    _, fields = wfdb.srdsamp(onda, pbdir=pbdir, sampto=1)
    signal_ii = fields['signame'].index("II")
    sfrom = wave['from']-20
    sto = wave['to']
    original = wfdb.rdsamp(onda, pbdir=pbdir, channels=[signal_ii],
                               sampfrom=sfrom, sampto=sto).p_signals
    original = original[~np.isnan(original)]
    save_word(original, wave['word'])
    return original

def find_word(word, dbname="mimic"):
    """finds the begin, the end a record that represents the word .
    word -- the word that we are searching
    """
    lenword=len(word)
    strlenword = str(lenword)
#    print(lenword)
    conn = psycopg2.connect("dbname="+dbname)
    cur = conn.cursor()
    select_statement = ("SELECT v1.r_s,v"+strlenword+
    '''.q_s,v1.record,a.rec_from
    FROM rstq v1
    INNER JOIN a on a.record=v1.record''')
    for i in range(lenword-1):
        select_statement += (" INNER JOIN rstq v"+str(i+2)+" on v"+
        str(i+1)+".record=v"+str(i+2)+".record ")
    select_statement += ''' WHERE v1.centroid =%s '''
    for i in range(lenword-1):
        select_statement += (" AND v"+str(i+2)+".centroid=%s AND v"+
        str(i+1)+".id+1=v"+str(i+2)+".id ")
    select_statement += " AND v1.r_s<v"+strlenword+'''.q_s
    AND a.record NOT IN ('mimic2wdb/matched/s20354/s20354-2526-08-25-00-53',
    'mimic2wdb/matched/s14584/s14584-2721-07-20-18-49',
    'mimic2wdb/matched/s18413/s18413-3047-06-23-22-31',
    'mimic2wdb/matched/s16032/s16032-3339-07-31-12-58')
    LIMIT 1'''
    wordo = (word[0],)
    for i in range(1,lenword):
        wordo += (word[i],)
    print(cur.mogrify(select_statement,wordo))
    cur.execute(select_statement,wordo)
    select = []
    for row in cur:
        from_val = row[3]+row[0]
        to_val = row[3]+row[1]
        select = {'from':from_val, 'to':to_val, 'record':row[2], 'word':word}
    cur.close()
    conn.close()
    return select

def plot_word(words):
    """plot a list of words.
    word -- list of words that are wanted to plot
    """
    create_word()
    clean_word()
    fig_size = [15, 3]
    plt.rcParams["figure.figsize"] = fig_size
    regs = 6 if len(words) > 6 else len(words)
    for i in range(regs):
        word = words[i]['word']
        wave = select_word(word)
        if wave is None:
            word_rstq = find_word(word)
            wave = download_word(word_rstq)
        plt.title(str(words[i]))
        plt.plot(wave[:1000])
        plt.show()
