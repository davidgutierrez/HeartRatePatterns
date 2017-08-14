# -*- coding: utf-8 -*-
import urllib.request  # the lib that handles the url stuff
import wfdb # the lib that handles the physionet stuff
import numpy # the lib that handles the arrays stuff
from scidbpy import connect #the lib that handles the scidby stuff

def uploadToSDB(sigII,ondaName,sdb):
  array = numpy.asarray(sigII, dtype=float)
  arrayNonNan = array[~numpy.isnan(array)]
  if arrayNonNan.any():
    print("uploading: "+ondaName)
    sdb.input(upload_data=array).store(ondaName,gc=False)
  return;

def downloadWFDB(onda,carpeta,sdb,ondaName):
  sig, fields = wfdb.srdsamp(onda,pbdir='mimic2wdb/matched/'+carpeta)
  signalII = None
  try:
    signalII = fields['signame'].index("II")
  except ValueError:
    print(ondaName+" no contains Signal II")
  if(signalII!=None):
    uploadToSDB(sig[:,signalII],ondaName,sdb)
  return;

target_url = "https://www.physionet.org/physiobank/database/mimic2wdb/matched/RECORDS-waveforms" # url of the waveforms of physionet
data = urllib.request.urlopen(target_url) # it's a file like object and works just like a file

sdb = connect('http://localhost:8080') #the url of the scidb service
sdbarrays = dir(sdb.arrays)
for line in data: # files are iterable
    carpeta,onda = str(line).replace('b\'','').replace('\'','').replace('\\n','').split("/")
    ondaName = onda.replace("-", "_")
    print(ondaName)
    if ondaName not in sdbarrays:
      downloadWFDB(onda,carpeta,sdb,ondaName)
