# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 22:27:44 2021
@author: martin.andersson-li

Look at each inventory that will be added to MEAD and see if all ID:s within 
tables matches. 
"""

import os
import pandas as pd
import re
import time

os.chdir("P:/eDNA/MEAD/IncludedProjects")
rootDir=os.listdir()

PS=re.compile("Sample.csv$", flags = re.IGNORECASE)
PP=re.compile("project.csv$", flags = re.IGNORECASE)
PO=re.compile("(?<!Update)OTU_[0-9]{6}MiFish_MEAD.csv$", flags = re.IGNORECASE)

#PO=re.compile("MiFish_MEAD.csv$")
otu = []
project = []
sample = []
aVal = 0

rootDir=rootDir[9:len(rootDir)]

for aDir in rootDir:
    aList = os.listdir(os.getcwd()+"\\"+aDir)
    for x in aList:
        sHit=re.search(PS,x)
        oHit=re.search(PO,x)
        pHit=re.search(PP,x)
        if sHit:
            sample.append(x)
            aVal+=1
        if oHit:
            otu.append(x)
            aVal+=1
        if pHit:
            project.append(x)
            aVal+=1
        if aVal == 3:
            aVal = 0
            print("Comparing SampleID in folder: ", aDir)
            oFile=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+otu[0])
            pFile=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+project[0],sep=";")
            sFile=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+sample[0])
            oID=oFile["SampleID"].str.match("^((?!Lab).)*$", flags= re.IGNORECASE)
            ngID=[not y for y in oID]
            posFile=oFile[list(map(bool, oID))]
            negFile=oFile[list(map(bool, ngID))]
            print("Removed rows from OTU-table: ",negFile['SampleID'].unique())
            spSet=set(sFile['SampleID'])
            otSet=set(posFile['SampleID'])
            for x in posFile['SampleID'].unique():
                if x not in spSet:
                    print(f"This sampleID is missing in Sample-table: {x}")
            for y in sFile['SampleID'].unique():
                if y not in otSet:
                    print(f"This sampleID is missing in OTU-table: {y}")
            print("Do you want to save the updated OTU file? Y/N?")
            chkPoint=input()
            if chkPoint == "Y":
                oFile.to_csv(os.getcwd()+"\\"+aDir+"\\"+"Update"+otu[0])
                print("Updated file was stored at:\n", os.getcwd()+"\\"+aDir+"\\"+"Update"+otu[0],"\n\n")
                print("Continuing to next folder!\n")
                time.sleep(2)
                otu = []
                project = []
                sample = []
            else:
                print("Continuing to next folder!\n")
                time.sleep(2)
                otu = []
                project = []
                sample = []
        
MarVer=re.compile("OTU_[0-9]{6}MarVer3_MEAD.csv$")
MiFish=re.compile("(UpdateOTU_[0-9]{6}MiFish_MEAD.csv$|OTU_[0-9]{6}MiFish_MEAD.csv$)")

for aDir in rootDir:
    otuVal = 0
    print("\nChecking sampleID among OTU tables in", aDir)
    aList = os.listdir(os.getcwd()+"\\"+aDir)
    for x in aList:
        if re.search(MarVer, x):
            MarFile = x
            otuVal +=1
        if re.search(MiFish, x):
            FishFile = x
            otuVal +=1
        if otuVal == 2:
            print("Mismatching rows in", aDir, "")
            time.sleep(3)
            otuVal = 0
            marOtu = pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+MarFile)
            fshOtu = pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+FishFile)
            fishSet=set(fshOtu['SampleID'].unique())
            marSet=set(marOtu['SampleID'].unique())
            for mID in marSet:
                if mID not in fishSet:
                    print(mID)
            del(MarFile)
            del(FishFile)

df=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/102633_Triton/OTU_102633MarVer3_MEAD.csv", sep=',',index_col=False, usecols=range(1,16))
df1=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/102633_Triton/UpdateOTU_102633MiFish_MEAD.csv", sep=',', usecols=range(1,16))
df2=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/101724_GG/OTU_101724MiFish_MEAD.csv", sep=',')

df1=df1.iloc[:,0:14]
df1.shape
df.shape

df.info()
df1.info()

df.iloc[:,1:len(df.columns)]

out=pd.concat([df,df1], axis=0, join='inner')
len(out.columns)

#df.columns[0]=="ProjectID"


storeFrame.shape

ggFish=pd.read_csv(os.getcwd()+"/102368_GG/UpdateOTU_102368MiFish_MEAD.csv")

ggFish.columns

njord=pd.read_csv(os.getcwd()+"/101808_Njord/OTU_101808MarVer3_MEAD.csv")
njord.columns == df2.columns


aX = pd.concat([storeFrame,fsDf], axis=0, join='inner')

#Construct the OTU-table for MEAD 
storeFrame=pd.DataFrame(columns=df2.columns)

for aDir in rootDir:
    aList = os.listdir(os.getcwd()+"\\"+aDir)
    for file in aList:
        if re.search(MarVer, file):
           print("\nJoining dataframe: ", file)
           mvFile = file
           mvDf=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+mvFile)
           if mvDf.columns[0] == "ProjectID":
               storeFrame = pd.concat([storeFrame,mvDf],axis=0,join='inner')
               print("Shape of OTU-frame is: ", storeFrame.shape)
               time.sleep(2)
           else:
               mvDf=mvDf.iloc[:,1:len(mvDf.columns)]
               storeFrame = pd.concat([storeFrame,mvDf], axis=0, join='inner')
               print("Shape of OTU-frame is: ", storeFrame.shape)
               time.sleep(2)
        if re.search(MiFish, file):
           print("\nJoining dataframe: ", file)
           fsFile = file
           fsDf=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+fsFile)
           if fsDf.columns[0] == "ProjectID":
               storeFrame = pd.concat([storeFrame,fsDf], axis=0, join='inner')
               print("Shape of OTU-frame is: ", storeFrame.shape)
               time.sleep(2)            
           else:
               fsDf=fsDf.iloc[:,1:len(fsDf.columns)]
               storeFrame = pd.concat([storeFrame,fsDf], axis=0, join='inner')
               print("Shape of OTU-frame is: ", storeFrame.shape)
               time.sleep(2)

typeSample=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/102368_GG/102368_Sample.csv", sep=',')


###Det är en missmatch pågrund av l och L i DNA columnen. 

df=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/101724_GG/101724_Sample.csv", sep=',')

len(df.columns)
typeSample.columns == df.columns

storeSample=pd.DataFrame(columns=typeSample.columns)
storeSample.columns  
           
#Construct the sampl-table for MEAD 
for aDir in rootDir:
    aList = os.listdir(os.getcwd()+"\\"+aDir)
    print("\nJoining sample-table in: ", aDir)
    for file in aList:
        if re.search(PS, file):
            smpDf=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+file)
            storeSample=pd.concat([storeSample,smpDf], axis=0, join='inner')
            print("Shape of OTU-frame is ", storeSample.shape)
            time.sleep(2)
            
        









#aDf=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/102368_GG/OTU_102368MarVer3_MEAD.csv", sep=',')
#aDf['SampleID']=aDf['SampleID'].str.replace("\W\([0-9]{4,5}\)", "")
#aDf['SampleID']=aDf['SampleID'].str.replace(" _", "_")
#aDf['SampleID'].unique()
#aDf.to_csv("P:/eDNA/MEAD/IncludedProjects/102368_GG/OTU_102368MarVer3_MEAD.csv", sep=',')


#TrList=['T01B_102633','T02B_102633','T02Y_102633','T04B_102633','T04Y_102633','T05B_102633','T06B_102633','T06Y_102633','T07B_102633','T07Y_102633','T08B_102633','T08Y_102633','T09B_102633','T09Y_102633','T10B_102633','T10Y_102633']
#NmList=["NMID11111	","NMID11112","	NMID11114","NMID11117","NMID11118","NMID11120","NMID11121","NMID11122","NMID11123","NMID11124","NMID11125","NMID11126","NMID11127","NMID11128","NMID11129","NMID11130"]
#            
#for newNm, oldNm in zip(TrList, MarDf['SampleID'].unique()):
#    MarDf['SampleID']=MarDf['SampleID'].str.replace(oldNm, newNm)
#
#        
#MarDf=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/102633_Triton/OTU_102633MarVer3_MEAD.csv", sep = ",")        
#MarDf.to_csv("P:/eDNA/MEAD/IncludedProjects/102633_Triton/OTU_102633MarVer3_MEAD.csv", sep=",")
#FisDf=pd.read_csv("P:/eDNA/MEAD/IncludedProjects/102633_Triton/UpdateOTU_102633MiFish_MEAD.csv", sep = ",")        
#MarDf['SampleID'].unique() 
#FisDf['SampleID'].unique() 



#pSl=re.compile("[0-9]{6}_Sample\.csv$")
#pOt=re.compile("OTU_[0-9]{6}[A-Za-z]+_MEAD.csv")
#pPj=re.compile("[0-9]{6}_project\.csv$")
#files = os.listdir(rootPth+"\\"+topFiles[0])            
#fileP=re.compile("(Sample.csv$|project.csv$|MiFish_MEAD.csv$)")

#aList = ["OTU_102634MiFish_MEAD.csv","102634_Sample.csv","102634_project.csv"]
#sample = []
#project = []
#otu = []
#aList = os.listdir(os.getcwd()+"\\"+rootDir[0])

#for subDir in os.listdir(os.getcwd()):
#    files = os.listdir(subDir)
#    if files
#    
#    for f in files:
#        if f.endswith('Sample.csv'):
#            sFile=pd.read_csv(os.getcwd()+"\\"+subDir+"\\"+f)
#            print(os.getcwd()+"\\"+subDir+"\\"+f)
#        if f.endswith('project.csv'):
#            pFile=pd.read_csv(os.getcwd()+"\\"+subDir+"\\"+f)
#            print(os.getcwd()+"\\"+subDir+"\\"+f)
#        if f.endswith('MEAD.csv'):
#            oFile=pd.read_csv(os.getcwd()+"\\"+subDir+"\\"+f)
#            print(os.getcwd()+"\\"+subDir+"\\"+f)

   
     
        
        
    #time.sleep(2)
#    for f in files:
#        if re.search(pSl,f):
#            sHit=re.search(pSl, f)
#            sFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+sHit[0])
#        if re.search(pOt, f):
#            oHit=re.search(pOt,f)
#            oFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+oHit[0])
#        if re.search(pPj, f):
#            pHit=re.search(pPj,f)
#            pFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+pHit[0], sep=";", nrows=1)
#        try:
#            oFile
#            pFile
#            sFile
#        except NameError:
#            continue
#        else:
#            print("\n\n",subDir)
#            print(rootPth+"\\"+subDir+"\\"+pHit[0])
#            print(rootPth+"\\"+subDir+"\\"+oHit[0])
#            print(rootPth+"\\"+subDir+"\\"+sHit[0])
#            oID=oFile["SampleID"].str.match("^((?!Lab).)*$")
#            ngID=[not y for y in oID]
#            posFile=oFile[list(map(bool, oID))]
#            negFile=oFile[list(map(bool, ngID))]
#            print("Removed rows from OTU-table: ",negFile['SampleID'].unique())
#            spSet=set(sFile['SampleID'])
#            otSet=set(posFile['SampleID'])
#            for x in posFile['SampleID'].unique():
#                if x not in spSet:
#                    print(f"This sampleID is missing in sample table: {x}")
#            for y in sFile['SampleID']:
#                if y not in otSet:
#                    print(f"This sampleID is missing in OTU-table: {y}")
#            del(oFile)
#            del(pFile)
#            del(sFile)
#            del(pHit)
#            del(sHit)
#            del(oHit)
#            
#            
        

#
#oFile.empty*1+sFile.empty*1+pFile.empty*1
#
#for subDir in os.listdir(os.getcwd()):
#    files = os.listdir(subDir)
#    if(re.search(pSl,files)):
#        
#    if:
#       sampleFile = sFile[0]
#    if 
#    
#    sDf=pd.read_csv(sFile[0])
#    oFile = re.search(pOt,files[2]) 
#    oDf = pd.read_csv(oFile[0])
#    thID=oDf["SampleID"].str.match("^((?!Lab).)*$")
#    ngID=[not y for y in thID]
#    posDf=oDf[list(map(bool, thID))]
#    negDf=oDf[list(map(bool, ngID))]
#    print("Removed rows from OTU-table: ",negDf['SampleID'].unique())
#    spSet=set(sDf['SampleID'])
#    otSet=set(posDf['SampleID'])
#    for x in posDf['SampleID'].unique():
#        if x not in spSet:
#            print(f"This sampleID is missing in sample table: {x}")
#    for y in sDf['SampleID']:
#        if y not in otSet:
#            print(f"This sampleID is missing in OTU-table: {x}")
#
#
#import os
#wd  = os.getcwd()
#directories = os.walk(wd)
#[print(x) for x in directories]

#for root, dirs in os.walk("P:/eDNA/MEAD/IncludedProjects"):
#    for aDir in dirs:
#        files=os.listdir()
#        sFile=re.search(pSl,files[1])
#        sDf=pd.read_csv(sFile[0])
#        oFile = re.search(pOt,files[2]) 
#        oDf = pd.read_csv(oFile[0])
#        thID=oDf["SampleID"].str.match("^((?!Lab).)*$")
#        ngID=[not y for y in thID]
#        posDf=oDf[list(map(bool, thID))]
#        negDf=oDf[list(map(bool, ngID))]
#        print("Removed rows from OTU-table: ",negDf['SampleID'].unique())
#        spSet=set(sDf['SampleID'])
#        otSet=set(posDf['SampleID'])
#        for x in posDf['SampleID'].unique():
#            if x not in spSet:
#                print(f"This sampleID is missing in sample table: {x}")
#            for y in sDf['SampleID']:
#                if y not in otSet:
#                    print(f"This sampleID is missing in OTU-table: {x}")
        
    
#
#len(chk["SampleID"].unique())
#len(oDf["SampleID"].unique())
#len(sDf['SampleID'])
#
#aX = "EY001F_101664" 
#bX=re.sub("EY[0-9]{3}[A-Z]{1}", "EY[0-9]{3}",aX)


#Read project data
#pPr=re.compile("[0-9]{6}_project\.csv$")
#pFile=re.search(pPr,files[0])
#pDf=pd.read_csv(pFile[0], sep=";", nrows=1)

#Store
#sDf.sort_values(by=["SampleID"], inplace=True)
#oDf.sort_values(by=["SampleID"], inplace=True)


#for subDir in os.listdir(os.getcwd()):
#    files=os.listdir(subDir)
#    for f in files:
#        if re.search(pSl,f):
#            sHit=re.search(pSl, f)
#            sFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+sHit[0])
#            print(sFile.head())


#for f in files:
#    if re.search(pSl,f):
#        sHit=re.search(pSl, f)
#        sFile=pd.read_csv(rootPth+"\\"+topFiles[0]+"\\"+sHit[0])
#    if re.search(pOt, f):
#        oHit=re.search(pOt,f)
#        oFile=pd.read_csv(rootPth+"\\"+topFiles[0]+"\\"+oHit[0])
#    if re.search(pPj, f):
#        pHit=re.search(pPj,f)
#        pFile=pd.read_csv(rootPth+"\\"+topFiles[0]+"\\"+pHit[0], sep=";", nrows=1)
#        
#print(pHit[0])
#print(sHit[0])
#print(oHit[0])

     


        


      
#for subDir in os.listdir(os.getcwd()):
#    files = os.listdir(subDir)
#    #time.sleep(2)
#    for f in files:
#        if re.search(pSl,f):
#            sHit=re.search(pSl, f)
#            sFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+sHit[0])
#        if re.search(pOt, f):
#            oHit=re.search(pOt,f)
#            oFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+oHit[0])
#        if re.search(pPj, f):
#            pHit=re.search(pPj,f)
#            pFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+pHit[0], sep=";", nrows=1)
#        try:
#            if oFile is not None and pFile is not None and sFile is not None:
#                oID=oFile["SampleID"].str.match("^((?!Lab).)*$")
#                ngID=[not y for y in oID]
#                posDf=oFile[list(map(bool, thID))]
#                negDf=oFile[list(map(bool, ngID))]
#                print("Removed rows from OTU-table: ",negDf['SampleID'].unique())
#                spSet=set(sFile['SampleID'])
#                otSet=set(posDf['SampleID'])
#                for x in posDf['SampleID'].unique():
#                    if x not in spSet:
#                        print(f"This sampleID is missing in sample table: {x}")
#                for y in sDf['SampleID']:
#                    if y not in otSet:
#                        print(f"This sampleID is missing in OTU-table: {x}")
#                del(oFile)
#                del(pFile)
#                del(sFile)
#                print("Ehh what?")
#        except Exception as e:
#                continue
            