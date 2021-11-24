# -*- coding: utf-8 -*-
"""
Create sample table from metadatafiles. 
"""

import os
import pandas as pd
import re
import numpy as np
import sys
import time
from unidecode import unidecode

#%reset -f

os.chdir("P:/eDNA/MEAD/Metadata/Sveavind/Gretas Klackar/2021/Maj/Sample")
pd.set_option("display.max_columns",30)
corCol=["SampleID","ProjectID","Lat","Long","Djup","DjupNivå","Datum","Tid","FiltreradVol","Temperatur","Delprov","ProvTyp","DNA_ng/uL","Fish_ng/uL","Vert_ng/uL"]

###Read in the metadata
val = 0
for file in os.listdir():
    if file.endswith(".xlsx") and val == 0:
        try:
            DNAfld=pd.read_excel(file)
            val = val+1
        except Exception as e:
            print(e)
        try:
            Waypoint=pd.read_csv("Koordinater_SWEREF99TM_Merged.csv", encoding = "latin-1") 
        except Exception as e:
            print(e)
        try:
            DNAcon=pd.read_csv("DNACon_Table.csv", encoding = "utf-8", sep=";")
            if DNAcon.shape[1] < 2:
                DNAcon=pd.read_csv("DNACon_Table.csv", encoding = "utf-8", sep=",")
        except Exception as e:           
            print(e)
        if Waypoint.shape[1] > 1 and DNAfld.shape[1] > 1 and DNAcon.shape[1] > 1:
            print("Metadata was succesfully loaded\n")
            print(f"Waypoints dimensions: {Waypoint.shape}")
            print(f"DNA concentration dimensions:{DNAcon.shape}")
            print(f"DNA field dimensions: {DNAfld.shape}")
            time.sleep(1)
        else: 
            print("All required data was not loaded. Exits script")
            sys.exit()
    
NegID=DNAfld['Sample number'].str.match(".+neg|^neg.+|.+RN$|.+FN$|.+FN_1$", flags = re.IGNORECASE)
if sum(NegID)>0:
    print("Negative sample found")
    time.sleep(2)
else: 
    print("No negative sample found. Print 'exit' to break or any key to continue:")
    noGo=input()
    if noGo == "exit":
        sys.exit()

NegSmp=DNAfld[list(map(bool,NegID))]

#Provide project ID
print("Enter projectID:")
prjID = input()

#Create column "Delprov" based on values in mL filtered
delList = []

for x in DNAfld['mL filtered']:
    if(x >= 2500) and (x <= 3499):
        delList.append(int(2))
    if(x >= 3500) and (x <= 5000):
        delList.append(int(3))
    if(x <= 1501):
        delList.append(0)        
        
DNAfld['Delprov'] = delList        
 
#Change column names in waypoint
Waypoint.rename(columns={'name':'Waypoint'}, inplace=True)
Waypoint = Waypoint[['xcoord', 'ycoord','Waypoint']]


#Merge and format field and waypoint data
MergeDf=DNAfld.merge(Waypoint, on='Waypoint')
MergeDf.rename(columns = {"Sample number":"SampleID"}, inplace=True)
MergeDf['SampleID']=MergeDf['SampleID'].str.replace("_","")

###Formats DNA concentration table###
#Checks if NM internal ID has been added
idChk = 0
nmID=re.compile("(?<![A-Z])([0-9]{1,2}_[0-9]{1,2})")
zP=re.compile("\(|\)")

print("Checks if NM internal ID has been added to sample ID and attempts to remove it.")
for sID in DNAcon['SampleID']:
    aReturn= re.match(nmID, sID)
    if aReturn and idChk == 0:
        print(DNAcon['SampleID'])
        print("\nPotential NM IDs found. Is this correct? Y/N")
        thResp = input()
        if thResp == "Y":
            idChk = idChk + 1
            DNAcon['SampleID']=DNAcon['SampleID'].str.replace(nmID, "", regex =True)
            DNAcon['SampleID']=DNAcon['SampleID'].str.replace(zP, "", regex = True)
        else:
            print("Original IDs were kept")
            idChk = idChk + 1
               
#Removes special character such as µ from columns
colList = []
for thCol in DNAcon.columns:
    newCol=unidecode(thCol)
    colList.append(re.sub("mL","uL", newCol))

DNAcon.columns = colList

DNAcon['SampleID'] = DNAcon['SampleID'].str.replace('_','')
DNAcon['SampleID'] = DNAcon['SampleID'].str.replace(' ','')
#Create column to seperate negativ from field samples 
p2 = re.compile("[A-Z][0-9]{2}(B|Y)$")
pX = re.compile("^[A-Z]{2,3}[0-9]{2,3}")
pN = re.compile("(.+neg|^neg.+|.+RN$|.+FN$|.+FN[0-9]{1}$)", flags=re.IGNORECASE)
negPosList = []

for smp in DNAcon['SampleID']:
    if bool(re.match(p2, smp)) == True:
        negPosList.append("Fältprov")
    elif bool(re.match(pX, smp)) == True:
        negPosList.append("Fältprov")
    elif bool(re.match(pN, smp)) == True:
        negPosList.append("Negativ")
    else: 
        negPosList.append("Okänt")

DNAcon['ProvTyp'] = negPosList 

#Split dataset between negative and field samples
NgID=DNAcon['SampleID'].str.match(".+neg|^neg.+|.+RN$|.+FN$|.+FN[0-9]{1}$", flags=re.IGNORECASE)
NegCon = DNAcon[list(map(bool, NgID))]
DNAcon = DNAcon[list(map(bool, [not elm for elm in NgID]))]

NegRow=pd.concat([NegCon.reset_index(drop=True), NegSmp.reset_index(drop=True)],axis=1)
NegRow.rename(columns = {"Sample":"SampleID","Collection date":"Datum", "Collection time":"Tid", "mL filtered":"FiltreradVol", "Depth":"Djup", "Temp":"Temperatur", "Sample":"SampleID", "Vertebrate ng/uL":"Vert_ng/µL", "Fish ng/uL":"Fish_ng/µL","DNA ng/ul":"DNA_ng/µL", "DNA_(ng/μl)":"DNA_ng/µL","Fish_(ng/μl)":"Fish_ng/µL"}, inplace=True)

aSet={"Y","B"}

depthList = []
for prov,typ in zip(DNAcon['SampleID'], DNAcon['ProvTyp']):
    if(typ == "Fältprov" and prov[-1] in aSet):
        depthList.append(prov[-1])
    else: depthList.append("NA")

DNAcon["DjupNivå"] = depthList

smpTable=MergeDf.merge(DNAcon, on='SampleID')
smpTable['ProjectID'] = prjID
smpTable['SampleID'] = smpTable['SampleID'].str.replace('_','')
smpTable['SampleID']=smpTable['SampleID']+"_"+smpTable['ProjectID']

smpTable.rename(columns = {"Sample":"SampleID","ycoord":"Lat", "xcoord":"Long","Collection date":"Datum", "Collection time":"Tid", "mL filtered":"FiltreradVol", "Depth":"Djup", "Temp":"Temperatur", "Sample":"SampleID", "Vertebrate ng/ul":"Vert_ng/uL", "Fish ng/ul":"Fish_ng/uL","DNA ng/uL":"DNA_ng/uL", "DNA_(ng/μl)":"DNA_ng/uL","Fish_(ng/μl)":"Fish_ng/uL"}, inplace=True)

NegRow=pd.concat([NegCon.reset_index(drop=True), NegSmp.reset_index(drop=True)],axis=1)

NegRow['ProjectID'] = prjID
NegRow['Lat'] = np.nan
NegRow['Long'] = np.nan
NegRow['Delprov'] = np.nan
NegRow['DjupNivå'] = np.nan
NegRow['SampleID']=NegRow['SampleID']+"_"+NegRow['ProjectID']

NegRow.rename(columns = {"Sample":"SampleID","Collection date":"Datum", "Collection time":"Tid", "mL filtered":"FiltreradVol", "Depth":"Djup", "Temp":"Temperatur", "Sample":"SampleID", "Vertebrate ng/ul":"Vert_ng/µl", "Fish ng/ul":"Fish_ng/µl","DNA ng/ul":"DNA_ng/µl", "DNA_(ng/μl)":"DNA_ng/µl","Fish_(ng/μl)":"Fish_ng/µl"}, inplace=True)

dropList = []
for aCol in NegRow.columns:
    if aCol not in corCol:
        dropList.append(aCol)
NegRow.drop(columns=dropList, inplace=True)    

dropList = []
for aCol in smpTable.columns:
    if aCol not in corCol:
        dropList.append(aCol)
smpTable.drop(columns=dropList, inplace=True)

smpTable = smpTable[corCol]
NegRow = NegRow[corCol]

smpTable=pd.concat([smpTable.reset_index(drop=True),NegRow.reset_index(drop=True)])
smpTable.rename(columns={"DNA_ng/uL":"DNA_ng/µL", "Fish_ng/uL":"Fish_ng/µL","Vert_ng/uL":"Vert_ng/µL)"}, inplace=True)

print(smpTable.head())
print(smpTable.tail())
print(smpTable.info())

print("Check sample data summary. If data is correct enter any key, else type 'exit'")
if input() != "exit":
    smpTable.to_csv(os.getcwd()+"\\"+prjID+"_Sample.csv", index = False)
    print(f"Sample data was merged and stored at:\n{os.getcwd()}\\{prjID}_Sample.csv")
else:
    print("Data was flaged as incorrect by user, run script line by line to locate errors")