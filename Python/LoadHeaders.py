import urllib.request
import wfdb
import psycopg2
from psycopg2.extensions import AsIs

def track_not_exists(cur, subject_id,recordDate):
    select_stament = 'select id from '+table+' where subject_id= %s and recorddate = %s'
    val = cur.execute(select_stament,(int(subject_id),recordDate))
    return cur.fetchone() is None

conn = psycopg2.connect("dbname=test")
cur = conn.cursor()
table = "waveformFields"

cur.execute("CREATE TABLE IF NOT EXISTS "+table+
            " (id serial PRIMARY KEY, comments character varying(255)[],"+
            " fs integer, signame character varying(255)[],"+
            " units character varying(255)[], subject_id integer,"+
            " recordDate character varying(255));")

target_url = "https://physionet.org/physiobank/database/mimic3wdb/matched/RECORDS-waveforms"
data = urllib.request.urlopen(target_url) # it's a file like object and works just like a file
for line in data: # files are iterable
	carpeta,subCarpeta,onda = str(line).replace('b\'','').replace('\'','').replace('\\n','').split("/")
	carpeta = carpeta+"/"+subCarpeta
	subject_id = subCarpeta.replace('p','')
	recordDate = onda.replace(subCarpeta+"-","")
	if track_not_exists(cur,subject_id,recordDate):
		print("inserting: ",onda)
		try:
			sig, fields = wfdb.srdsamp(onda,pbdir='mimic3wdb/matched/'+carpeta, sampto=1)
			fields['subject_id'] = subject_id
			fields['recordDate'] = recordDate
			columns = fields.keys()
			values = [fields[column] for column in columns]
			insert_statement = 'insert into '+table+' (%s) values %s'
			cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
			conn.commit()
			print("inserted: ",onda)
		except ValueError as inst:
    			print("onda vacia")
conn.close()
