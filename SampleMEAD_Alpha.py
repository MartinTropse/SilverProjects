
# -*- coding: utf-8 -*-
"""
Create sample table from metadatafiles. 
"""

#import camelot
#from PyPDF2 import PdfFileReader
import tabula
import os
import pandas as pd
import re
import numpy as np
import time



os.chdir("P:/eDNA/MEAD/Metadata/OX2/Aurora/2021_03_Mar/Sample")

###Read in sammple Data
pX=re.compile(".+\.xlsx")

for file in os.listdir():
    if file.endswith(".xlsx"):
        DNAfld=pd.read_excel(file)


pn=re.compile("neg", flags=re.IGNORECASE)
NegID=DNAfld['Sample number'].str.match(".+neg$", flags = re.IGNORECASE)
NegSmp=DNAfld[list(map(bool,NegID))]

#Provide project ID
prjID = input()

#Create column "AntalDelProv" based on values in mL filtered
delList = []

for x in DNAfld['mL filtered']:
    if(x >= 2500) and (x <= 3499):
        delList.append(int(2))
    if(x >= 3500) and (x <= 5000):
        delList.append(int(3))
    if(x <= 1501):
        delList.append(0)        
        
DNAfld['Delprov'] = delList        
 
Waypoint=pd.read_csv("Koordinater_SWEREF99TM_Merged.csv", encoding = "latin-1") 

Waypoint.columns
Waypoint.rename(columns={'name':'Waypoint'}, inplace=True)
Waypoint = Waypoint[['xcoord', 'ycoord','Waypoint']]

MergeDf=DNAfld.merge(Waypoint, on='Waypoint')
MergeDf.rename(columns = {"Sample number":"Sample"}, inplace=True)
#MergeDf.drop(columns=['Waypoint'], index=1, inplace=True)

#pdf = PdfFileReader(open(file,'rb'))
#pdf.getNumPages()
#
#for x in range(1,pdf.getNumPages()):
#    tables = camelot.read_pdf(file,flavor='stream', page = x)
#    for y in range(0, tables.n-1):
#        print(tables[y].df)
#
#chk=camelot.read_pdf(file,flavor='stream', page = 9)
#
#DNAcon=tables[0].df
#DNAcon=DNAcon.iloc[5:25,[0,2,3]] 
#
#DNAcon.rename(columns = {0:'Sample', 2:'DNA/ul', 3:'(ng/ul)'}, inplace=True)
#DNAcon['Sample'] = DNAcon['Sample'].str.replace('\)','', regex =True)

###Extract pdf from table###        
val = 0
for files in os.listdir():
    if files.endswith(".pdf") and val == 0:
        tables1 = tabula.read_pdf(files, pages="all")
        val +=1
        tabFile1 = files
    elif files.endswith(".pdf") and val > 0:
        tables2 = tabula.read_pdf(files, pages="all")
        print("Found second pdf report!")
        tabFile2 = files

###Write loop that identifies DNA-conc table###
p=re.compile("DNA.+\(ng")

for num in range(0,len(tables1)):
    for col in tables1[num].columns:
       if bool(re.match(p, col)) == True:
           DNAcon = tables1[num]
           print(tables1[num])




DNAcon.dropna(inplace=True, axis=1)

nmList=['Sample', 'Volume','Date arrived', 'DNA ng/ul', 'Vertebrate ng/ul', 'Fish ng/ul']

for x, y in zip(DNAcon.columns, nmList):
    if len(DNAcon.columns == len(nmList)):
        DNAcon.rename(columns= {x:y},inplace=True)

smplList = []
p1=re.compile("(?<=\().+(?=\))")

for x in range(0, len(DNAcon['Sample'])):
    aMatch=re.search(p1, DNAcon['Sample'][x])
    if len(aMatch[0])>0:
        smplList.append(aMatch[0])
    else: print("ops")    

DNAcon['Sample'] = smplList

#Create column to seperate negativ from field samples 
p2 = re.compile("[A-Z]_[0-9]{2}_(B|Y)$")
negPosList = []

for smp in DNAcon['Sample']:
    if bool(re.match(p2, smp)) == True:
        negPosList.append("Fältprov")
    else:
        negPosList.append("Negativ")

DNAcon['ProvTyp'] = negPosList 
DNAcon.drop(columns=["Volume", "Date arrived"], index=1, inplace=True)

depthList = []
for prov,typ in zip(DNAcon['Sample'], DNAcon['ProvTyp']):
    if(typ == "Fältprov"):
        depthList.append(prov[-1])
    else: depthList.append("NA")

DNAcon["DjupNivå"] = depthList






smpTable=MergeDf.merge(DNAcon, on='Sample')
smpTable.drop(columns=["Waypoint","Collector", "Analysis", "Unnamed: 9"], inplace=True)

smpTable['ProjectID'] = prjID
smpTable['Sample'] = smpTable['Sample'].str.replace('_','')

smpTable['SampleID']=smpTable['SampleID']+"_"+smpTable['ProjectID']
smpTable.rename(columns = {"xcoord":"Long","ycoord":"Lat", "Collection date":"Datum", "Collection time":"Tid", "mL filtered":"FilteradVol", "Depth":"Djup", "Temp":"Temperatur", "Sample":"SampleID", "Vertebrate ng/ul":"Vert_ng/µl", "Fish ng/ul":"Fish_ng/µl","DNA ng/ul":"DNA_ng/µl"}, inplace=True)
smpTable.info()

smpTable=smpTable [["SampleID","ProjectID","Lat","Long","Djup","DjupNivå","Datum","Tid", "FilteradVol","Temperatur","Delprov","ProvTyp","DNA_ng/µl", "Fish_ng/µl","Vert_ng/µl"]]

#Add lines for negative samples
NgID=DNAcon['Sample'].str.match(".+_neg$", flags=re.IGNORECASE)
NegCon = DNAcon[list(map(bool, NgID))]
NegRow=pd.concat([NegCon.reset_index(drop=True), NegSmp.reset_index(drop=True)],axis=1)
NegRow.drop(columns=["Waypoint","Collector", "Analysis", "Unnamed: 9", "Sample number"], inplace=True)
NegRow['ProjectID'] = prjID
NegRow['Lat'] = np.nan
NegRow['Long'] = np.nan
NegRow['Delprov'] = np.nan

NegRow.rename(columns = {"Sample":"SampleID","Collection date":"Datum", "Collection time":"Tid", "mL filtered":"FilteradVol", "Depth":"Djup", "Temp":"Temperatur", "Sample":"SampleID", "Vertebrate ng/ul":"Vert_ng/µl", "Fish ng/ul":"Fish_ng/µl","DNA ng/ul":"DNA_ng/µl"}, inplace=True)

NegRow.info()
NegRow=NegRow[["SampleID","ProjectID","Lat","Long","Djup","DjupNivå","Datum","Tid", "FilteradVol","Temperatur","Delprov","ProvTyp","DNA_ng/µl", "Fish_ng/µl","Vert_ng/µl"]]

smpTable=pd.concat([smpTable.reset_index(drop=True),NegRow.reset_index(drop=True)])

smpTable.to_csv(os.getcwd()+"\\"+prjID+"_Sample.csv", index = False)

