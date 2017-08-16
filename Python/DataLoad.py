# -*- coding: utf-8 -*-
import urllib.request  # the lib that handles the url stuff
import wfdb # the lib that handles the physionet stuff
import numpy # the lib that handles the arrays stuff
import gc
from scidbpy import connect #the lib that handles the scidby stuff
from sklearn.preprocessing import normalize

def uploadToSDB(sigII,ondaName,sdb):
  array = numpy.asarray(sigII, dtype=float)
  arrayNonNan = array[~numpy.isnan(array)]
  arrayNonNan = numpy.trim_zeros(arrayNonNan)
  if arrayNonNan.any():
    print("uploading: "+ondaName)
    array = normalize(arrayNonNan[:,numpy.newaxis], axis=0).ravel()
    sdb.input(upload_data=array).store(ondaName,gc=False)
  return;

def downloadWFDB(onda,carpeta,sdb,ondaName):
  signalII = None
  try:
    sig, fields = wfdb.srdsamp(onda,pbdir='mimic2wdb/matched/'+carpeta, sampto=1)
    channel = fields['signame'].index("II")
    if(channel!=None):
      sig, fields = wfdb.srdsamp(onda,pbdir='mimic2wdb/matched/'+carpeta, channels = [channel])
      print("downloaded:" + ondaName)
      uploadToSDB(sig[:,0],ondaName,sdb)
  except ValueError:
    print(ondaName+" no contains Signal II")
  return;

def fillReadedWaves(sdb):
  file = open("Jupyter/readedWaves.txt","r")    
  arrays = dir(sdb.arrays)
  filelines = file.readlines()
  arrays.extend([w.replace('\n','') for w in filelines])
  return arrays;

target_url = "https://www.physionet.org/physiobank/database/mimic2wdb/matched/RECORDS-waveforms" # url of the waveforms of physionet
data = urllib.request.urlopen(target_url) # it's a file like object and works just like a file

sdb = connect('http://localhost:8080') #the url of the scidb service
sdbarrays = fillReadedWaves(sdb)
for line in data: # files are iterable
    gc.collect()
    file = open("Jupyter/readedWaves.txt","a") 
    carpeta,onda = str(line).replace('b\'','').replace('\'','').replace('\\n','').split("/")
    ondaName = onda.replace("-", "_")
    print(ondaName)
    if ondaName not in sdbarrays:
      file.write(ondaName+"\n")
      downloadWFDB(onda,carpeta,sdb,ondaName)
      file.close()
