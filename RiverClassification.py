# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:33:39 2019
@author: BigTail

Data analyzis script that summarize data of rivers in Östergötland.
It checks for questions such as the area affected by drenching, 
how affected the river is by human fysical alteration, the percentage landtypes 
that occurs along the rivers and so forth.  

The results of the script was used in the EU-water classification of 2018 and stored in VISS. 
"""

import os
import time
import pandas as pd 
import numpy as np
import re

os.chdir("C:/Py3/TempHymo/Script")
path=os.getcwd()

file = "HymoDataSummary.csv"
Hymo = pd.read_csv("CleanBigData.csv", sep = ',', header=0)

Hymo.Paverkan = Hymo.Paverkan.astype("str")
hcol=Hymo.columns
run = "seconds. Moving onwards!"

EUList=Hymo.EU_CD.unique().tolist()  
Nr=list(range(0,len(EUList))) 
df = pd.DataFrame(np.nan, index = Nr, columns = [''])

Hymo.Paverkanst.unique()
# =============================================================================
# #Transform data to mutibable int and str
# =============================================================================
#Hymo['Shape_Leng'].dtype
Hymo.info()


try:
    for y in Hymo.columns:
        if(Hymo[y].dtype == "int64" or Hymo[y].dtype == "int32" or Hymo[y].dtype == "float64" or Hymo[y].dtype == "float32"):
              Hymo[y]=Hymo[y].astype('int')
        else:
             Hymo[y]=Hymo[y].astype('str')
except Exception as e:
    print(e)
 

count=0
for x in Hymo.columns:
    if x != 'Kommentar':
        print(Hymo.columns[count], Hymo['{}'.format(x)].unique(),"\n")
        count +=1


# =============================================================================
# #Adds HARO ID 
# =============================================================================
HaroList = []
start = time.time() 
       
try:
    for x in EUList:
       Temp=Hymo.loc[Hymo['EU_CD'] == '{}'.format(x)]
       HaroList.append(Temp.Haro.unique()) 
except Exception as e:
    print(e)
            
df['Haro'] = HaroList
df = df.iloc[:,1].to_frame()

elapse0 = int(time.time() - start) 
print("First operation took", int(elapse0), run)

# =============================================================================
# #Uses a 2D list to collect information on lenght, lakes, affected etc by EU_CD
# =============================================================================
for x in range(min(Hymo.index),max(Hymo.index)):
    if Hymo.Kommentar[x] == "Sjö":
        Hymo.Paverkad[x] = "Sjö"
        print(x)


StoreList = [[],[],[],[]]
StoreList = [[] for x in len(Hymo.Paverkad.unique())]

seq=Hymo.Paverkad.unique()

a=[seq[i:i] for i in range(0,len(seq))]

for x in a:
    append("")

ShapeList = []
PvrknList=Hymo.Paverkad.unique().tolist()

Hymo.Paverkad.value_counts()
Hymo.Paverkad.unique()

start = time.time()
try:
    for x in EUList:
        EU=Hymo.loc[Hymo['EU_CD'] == '{}'.format(x)]
        ShapeList.append(EU.Shape_Leng.sum())
        count = 0
        for y in PvrknList:
            Act = EU.loc[EU['Paverkad'] == '{}'.format(y)]
            StoreList[count].append(Act.Shape_Leng.sum())
            count += 1
except Exception as e:
    print(e)
elapse1 = int(time.time() - start) 
print("Second operation took", int(elapse1), run)
        

# =============================================================================
# Testing function
# =============================================================================
AfctTypeList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
Hymo.Paverkanst=Hymo.Paverkanst.replace('nan', '<Null>')

ListPos = 0
ImpList = Hymo.Paverkanst.unique()
Hymo.Paverkanst.value_counts()

sum(AfctTypeList[2])

start = time.time()
try:
    for x in EUList:
        EU=Hymo.loc[Hymo['EU_CD'] == '{}'.format(x)]
        TotSum =EU.Shape_Leng.sum()
        ListPos = 0
        for y in ImpList:            
             holder=EU.loc[EU['Paverkanst'] == '{}'.format(y)]
             AfctTypeList[ListPos].append(holder.Shape_Leng.sum())
             ListPos += 1
except Exception as e:
    print(e)

elapse2 = int(time.time() - start) 
print("Third operation took", int(elapse2), run)
# =============================================================================
# Look at the percentage waterobject that is biotopmapped
# =============================================================================
# =============================================================================
Hymo.Biotopkart.unique()
Hymo.Biotopkart.value_counts()

BiList=[[],[]]
start = time.time()

try:
    for x in EUList:
        #count = -1
        EU=Hymo.loc[Hymo['EU_CD'] == '{}'.format(x)]
        #print("Well at least we got one more!\n" )
        NegEU=EU[(EU['Biotopkart'] == "Nej")|(EU['Biotopkart'] == "<Null>")]
        PosEU=EU[(EU['Biotopkart'] != "Nej")&(EU['Biotopkart'] != "<Null>")]
        sum(PosEU.Shape_Leng)
        BiList[0].append(sum(NegEU.Shape_Leng))
        BiList[1].append(sum(PosEU.Shape_Leng))
except Exception as e:
    print(e)    

tid = int(time.time()-start) 
print("Summarizing biotopkartering took: ",tid, "sec")

del(PosEU)
del(NegEU)

# =============================================================================
# #Summarize types of biotopkatering
# =============================================================================
BioUniq = Hymo.Biotopkart.unique().tolist()
BioStore=[BioUniq[i:i] for i in range(0,len(BioUniq))]  
TwoThr = [[],[]]
OneZero = [[],[]]

for x in EUList:
    EU = Hymo[(Hymo['EU_CD'] == '{}'.format(x)) & (Hymo.Biotopkart != "<Null>")]
    ID = 0
    for y in BioUniq:
        SEU=EU.loc[EU['Biotopkart'] == "{}".format(y)]
        if y == "23":
            TwoThr[0].append(sum(SEU.Shape_Leng)/2)
            TwoThr[1].append(sum(SEU.Shape_Leng)/2)
            ID += 1
        elif y == "01":
            OneZero[0].append(sum(SEU.Shape_Leng)/2)
            OneZero[1].append(sum(SEU.Shape_Leng)/2) 
            ID += 1
        else:
            a=sum(SEU.Shape_Leng)
            BioStore[ID].append(a)
            ID += 1

out100=np.asarray(OneZero[0])
out101=np.asarray(OneZero[1])
out230=np.asarray(TwoThr[0])
out231=np.asarray(TwoThr[1])
bout3=np.asarray(BioStore[2])
bout2=np.asarray(BioStore[5])
bout1=np.asarray(BioStore[4])
bout0=np.asarray(BioStore[3])

#Strange code, but it takes arrays and add half of the values of length from the 23 and 01 categories in biotopkart
Update3=list(bout3+out230)
Update2=list(bout2+out230)
Update0=list(bout0+out100)
Update1=list(bout1+out100)
BioStore[2] = Update3
BioStore[5] = Update2
BioStore[4] = Update1
BioStore[3] = Update0
# =============================================================================
# # #Gather information on types of Paverkan 1-7 as a percent of total length 
# =============================================================================
PavkanTypeList = [[],[],[],[],[],[],[],[]]
PavkanListan = [[] for x in range(len(Hymo.Paverkan.unique()))]
ListPos = 0
TypeList = Hymo.Paverkan.unique()

start = time.time()
try:
    for x in EUList:
        EU=Hymo.loc[Hymo['EU_CD'] == '{}'.format(x)]
        TotSum =EU.Shape_Leng.sum()
        ListPos = 0
        for y in TypeList:
             holder=EU.loc[EU['Paverkan'] == '{}'.format(y)]
             PavkanTypeList[ListPos].append(((holder.Shape_Leng.sum())/TotSum)*100)
             PavkanListan[ListPos].append((holder.Shape_Leng.sum()))
             ListPos += 1
except Exception as e:
    print(e)

elapse35 = int(time.time() - start) 
print("Operation 3.5 took", int(elapse35), run)

# =============================================================================
# #Summarize the type of MAVF that occurs in the area and store as string
# =============================================================================
MarkTypList = []

start=time.time()
try:
    for x in EUList:
        imdvf=Hymo[Hymo['EU_CD'] == '{}'.format(x)]
        #imdvf=idmvf[(idmvf.MAVFtyp != '<Null>')]    
        UnikList=imdvf.MAVFtyp.unique().tolist()
        TempVar = ': '.join(UnikList)
        MarkTypList.append(TempVar)    
            #MarkTypList.append(join(UnikList))
except Exception as e:
    print(e)
elapse3= int(time.time() - start)
print("Fourth operation took", elapse3, run)

# =============================================================================
# #Calculates the length the MAVF affected regions 
# =============================================================================
MAVList = [[],[],[]]
UnikMav=Hymo.MAVF.unique().tolist()

start = time.time()
try:
    for x in EUList:
        ideu=Hymo[Hymo['EU_CD'] == '{}'.format(x)]
        count = 0
        for y in UnikMav:
            g=ideu.loc[ideu['MAVF'] == '{}'.format(y)]
            MAVList[count].append(g.Shape_Leng.sum())
            count += 1;    
except Exception as e:
    print(e)

elapse4= int(time.time() -start)
print("Fifth operation took", elapse4, run)            

# =============================================================================
# #Check the fraction of MVF in each agriculture region per EU_CD  
# =============================================================================
Hymo.MAVF.unique()
Hymo.Shape_Leng.unique()

start = time.time()
MAVF_JordL = []

for x in EUList:
    dfFirst=Hymo[Hymo['EU_CD'] == '{}'.format(x)]
    g=dfFirst.loc[dfFirst['Paverkanst'] == 'Jordbruk']
    SumJd=sum(g.Shape_Leng)
    if SumJd > 0:
        #print("Jordbruk summa: ", SumJd)
        g2=g.loc[g['MAVF'] == "Ja"]
        SumMV=sum(g2.Shape_Leng)
        if SumMV > 0:
            #print("MAVF summa: ", SumMV)
            MAVF_JordL.append((SumMV/SumJd)*100)
        else: 
            MAVF_JordL.append(0)
    else:
        MAVF_JordL.append("IngetJordbruk")            

#df['MAVF_Jordbruk'] = MAVF_JordL


MAVF_JordL            
# =============================================================================
# #Creates the seconday data dataframe 
# =============================================================================
TypeList = Hymo.Paverkanst.unique()


df['EU_CD'] = EUList
df['VattenLangd'] = ShapeList
df['SjoLangd'] = StoreList[3]
df['VattenMinusSjo'] = (df['VattenLangd']-df['SjoLangd'])
df['OP_Langd'] = StoreList[0]
df['Oklassad'] = StoreList[2]  
df['P_Langd'] = StoreList[1]  

df['P%'] =((df.P_Langd/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Jrdb%'] =((df.Jordbruk/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
a =((df.Jordbruk/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
b = ((df.Skogsbruk/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Skgb%'] = ((df.Skogsbruk/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Foraldrad_Okand%'] =((df['Föråldrad eller okänd']/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Flottning%'] =((df.Flottning/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Transport%'] =((df.Transport/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Urban%'] =((df.Urban/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['JordbrukOSkogsbruk%'] =((df['Jordbruk och skogsbruk']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))
df['Vattenkraft%'] =((df.Vattenkraft/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Rekreation%'] =((df.Rekreation/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['OversvamSkydd%'] =((df.Översvämningsskydd/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Sjofart%']=((df.Sjöfart/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Flygbana_forsvar%']=((df['Flygbana, försvaret']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))
df['MVF_Langd'] = MAVList[1]
df['MAVF_JordL'] = MAVF_JordL 
df['MVF%'] = ((df['MVF_Langd']/df.VattenLangd - (df.Oklassad+df.SjoLangd)*100).astype(float)) # add new col name
df['MVF_Typ'] = MarkTypList

df['0%'] =((df['0']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))
df['1%'] =((df['1']/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['2%'] =((df['2']/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['3%'] =((df['3']/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['4%']=((df['4']/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['5%']=((df['5']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))
df['5%']=((df['5']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))
df['4%']=((df['4']/(df.VattenLangd - (df.SjoLangd+df.Oklassad))*100).astype("float"))
df['Sjo%']=((df['sjö']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))


df2=df.sort_values(by="Haro", ascending=False)
Hymo.Paverkan.value_counts()
ListPos = 0
TypeList = Hymo.Paverkan.unique()

#Distance PavkanType Percentage of total length 
count=0
for x in TypeList:
    df['{}%'.format(x)] = PavkanTypeList[count]
    count+=1
else:
    count+=1


#Distance PavkanListan of total length
count=0
for x in TypeList:    
    df['{}'.format(x)] = PavkanListan[count]
    count+=1
else:
    count+=1

df.to_csv("Checking_Rattning.csv", sep=',', header=1)


df['PVarde0_Naturlig'] = PavkanTypeList[0]
df['PVarde1_Ratat'] =  PavkanTypeList[1]
df['Oklassd_rattning'] = PavkanTypeList[2]
df['PVarde2_Kulvert'] = PavkanTypeList[3]
df['PVarde3_Damme'] =  PavkanTypeList[2] 
df['PVarde4_Inval'] =  PavkanTypeList[4]
df['PVarde5_RattngInUtLopp'] =  PavkanTypeList[6]
df['Biotopkartad'] = BiList[1]
df['Ej_Biotopkartad'] = BiList[0]
df['Biotop%']=((df['Biotopkartad']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))
((df['sjö']/(df.VattenLangd - (df.Oklassad+df.SjoLangd))*100).astype("float"))

df['Biotop0'] = BioStore[3]
df['Biotop1'] = BioStore[4]
df['Biotop2'] = BioStore[5]
df['Biotop3'] = BioStore[2]


# =============================================================================
# #Check if a EU_CD has either more or less then  15 affected and adds matching string 
# #And check if each affect type is more then 3% before that
# =============================================================================
df.columns.get_loc("Jrdb%")
df.columns.get_loc("Flygbana_forsvar%") 

t1=df.iloc[:,32]
  
DfAffect = df.iloc[:,22:33]
DfAffect['JrdSkog%'] = df.iloc[:,35]
ValueList = []

start = time.time()
try:
    for x in range(DfAffect.shape[0]):
        value = 0
        for y in range(0,len(DfAffect.columns)):
            if DfAffect.iloc[x,y] > 3:
                value += DfAffect.iloc[x,y]
        ValueList.append(value)
except Exception as e:
    print(e)        

elapse5 = int(time.time() - start) 
print("Sixth operation took", elapse5, run)        

DfAffect['Sum'] = ValueList                    
df['PavrkdSum'] = ValueList

for x in df.columns:
    if df['{}'.format(x)].dtype == "float64":
        df['{}'.format(x)]=df['{}'.format(x)].round(1)
        

Sec=elapse0+elapse1+elapse2+elapse3+elapse4+elapse5+elapse35
df=df.sort_values('Haro', ascending = False)
df.to_csv("HymoPart3Summary.csv", sep = ',', header=1, index = False)
os.getcwd()
 
print("\nAnalysis is done! Run time:", Sec, "seconds")
print("\nResults is saved at", path+"\\"+file)
print("\nAbbreviations: P = Paverkad; MVF = Markavvattningsföretag")

Hymo.Paverkan.unique()
sum(Hymo.Paverkanst.value_counts())
sum(Hymo.Paverkad.value_counts())