# -*- coding: utf-8 -*-
import urllib.request  # the lib that handles the url stuff
import wfdb # the lib that handles the physionet stuff
import numpy # the lib that handles the arrays stuff
from scidbpy import connect #the lib that handles the scidby stuff

target_url = "https://www.physionet.org/physiobank/database/mimic2wdb/matched/RECORDS-waveforms" # url of the waveforms of physionet
data = urllib.request.urlopen(target_url) # it's a file like object and works just like a file

sdb = connect('http://localhost:8080') #the url of the scidb service
sdbarrays = dir(sdb.arrays)
for line in data: # files are iterable
    carpeta,onda = str(line).replace('b\'','').replace('\'','').replace('\\n','').split("/")
    ondaName = onda.replace("-", "_")
    print(ondaName)
    if ondaName not in sdbarrays:
        sig, fields = wfdb.srdsamp(onda,pbdir='mimic2wdb/matched/'+carpeta) #, sampfrom=11000#sig, fields = wfdb.srdsamp('s00001-2896-10-10-00-31',pbdir='mimic2wdb/matched/s00001', sampfrom=11000)
        signalII = None
        try:
                signalII = fields['signame'].index("II")
        except ValueError:
    	        print("List does not contain value")
        if(signalII!=None):
                array = numpy.asarray(sig[:,signalII], dtype=float)
                arrayNonNan = array[~numpy.isnan(array)]
                if arrayNonNan.any():
            	        print("non empty "+ondaName)
            	        sdb.input(upload_data=array).store(ondaName,gc=False)
