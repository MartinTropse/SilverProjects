from urllib2 import urlopen
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os
import bs4 as bs
import time
import re
import sys

os.chdir("C:/Py27")
df=pd.read_csv("Fast_test.csv", sep=';', header=0, encoding='windows-1252')
df=df.iloc[0:10, :]

nr = range(0, len(df['EXLINK']))

tidobj= time.localtime()
datum = time.strftime('%Y-%m-%d__%H%M', tidobj)

os.mkdir("Kontakt/"+datum)
os.chdir("Kontakt/"+datum)

PerList = []

for fast in df['EXLINK']: 
    url = fast
    html = urlopen(url).read()
    soup = bs.BeautifulSoup(html, features="html.parser")
    lsub = soup.find('table', id='lagfart')
    if lsub is None:
        PerList.append("Information Saknas")
        print "Ingen Info"
    else:
        person = lsub.find('table', id=re.compile(r'(person|organisation)'))
        taxDel=soup.find('table', {"id":"MainContent_TaxeringDirektControl_TableTaxeringsdel"})
        if person:
            print "En person/Organisation"
            person = person.text
            PerList.append(person)
            time.sleep(0.1)
        elif taxDel:
            print "Endast taxeringsuppgift"
            taxDel=taxDel.text
            PerList.append(taxDel)
            time.sleep(0.1)            
        else:
            print "Lagfart saknas"
            PerList.append("Ingen Lagfart")
            time.sleep(0.1)
                

for x in range(0, len(PerList)):
    PerList[x]=re.sub(r'\n+', '\n', PerList[x])

for x in range(0, len(PerList)):
    PerList[x]=re.sub(r'(.*?(\nAdress.*?){1})\nAdress', r'\1 Alternativ adress ', PerList[x])

Pernr = []
Fnamn = []
Tnamn = []
Enamn = []
Adres = []
Pstnr = []
Pstor = []

Opos = []
Opnr = []
Oonr = []
Oonm = []
Ojrf = []
Oadr = []

Ppnr = []
Pfnm = []
Penm = []
Ptnm = []
Padd = []
Puadd = []
Pstnr = []
Port = []
Plnd = []

Txlist = []

Type = []

for x in PerList:
    org=re.search("Organisationsnummer", x)
    per=re.search("Personnummer", x)
    noi=re.search("Information Saknas", x)
    txu=re.search("Taxeringsdel", x)
    if org:
        Type.append("Organisation")
        pnr=re.search(r'Postnummer:.+?(?=\n)', x)
        opo=re.search(r'Postort:.+?(?=\n)', x)
        onm=re.search(r'Organisationsnamn:.+?(?=\n)', x)
        onr=re.search(r'Organisationsnummer:.+?(?=\n)', x)
        ojf=re.search(r'Juridisk form:.+?(?=\n)', x)
        oad=re.search(r'Adress:.+?(?=\n)', x)
        if pnr:
            Opnr.append(pnr.group(0))
        else:
            Opnr.append("PstNr Saknas")
        if opo:
            Opos.append(opo.group(0))
        else:
            Opos.append("PstOrt Saknas")
        if onm:
            Oonm.append(onm.group(0))
        else:
            Oonm.append("OrgNm Saknas")
        if onr:
            Oonr.append(onr.group(0))
        else:
            Oonr.append("OrgNr Saknas")
        if ojf:
            Ojrf.append(ojf.group(0))
        else:
            Ojrf.append("JurForm Saknas")
        if oad:
            Oadr.append(oad.group(0))
        else:
            Oadr.append("Adress Saknas")
    elif per:
        Type.append("Person")
        pper = re.search(r'Personnummer:.+?(?=\n)', x)
        pfor = re.search(r'F\xf6rnamn:.+?(?=\n)', x)
        ptnm = re.search(r'Tilltalsnamn:.+?(?=\n)', x)
        penm = re.search(r'Efternamn:.+?(?=\n)', x)
        padd = re.search(r'Adress:.+?(?=\n)', x)
        pstnr = re.search(r'Postnummer:.+?(?=\n)', x)
        port = re.search(r'Postort:.+?(?=\n)', x)
        plnd = re.search(r'Land:.+?(?=\n)', x)
        #palnd = re.search(r'Utdelningsadress:.+?(?=\n)', x)
        if pper:
            Ppnr.append(pper.group(0))
        else:
            Ppnr.append("Uppgift Saknas")
        if pfor:
            Pfnm.append(pfor.group(0))
        else:
            Pfnm.append("Uppgift Saknas")
        if ptnm:
            Ptnm.append(ptnm.group(0))
        else:
            Ptnm.append("Uppgift Saknas")
        if penm:
            Penm.append(penm.group(0))
        else:
            Penm.append("Uppgift Saknas")
        if padd:
            Padd.append(padd.group(0))
        else:
            Padd.append("Uppgift Saknas")
        if port:
            Port.append(port.group(0))
        else:
            Port.append("Uppgift Saknas")
        if pstnr:
            Pstnr.append(pstnr.group(0))
        else:
            Pstnr.append("Uppgift Saknas")
        if plnd:
            Plnd.append(plnd.group(0))
        else:
            Plnd.append("Sverige")
    elif txu:
        Type.append("Endast_Taxsuppgift")
        s = ""
        allTd=taxDel.find_all('td', {"class":"TextCell"})
        for x in allTd:
            x = x.text 
            s = s+" "+x
        Txlist.append(s)
    else:                   #Catch ingen info, and add missing info in per
        Type.append("Ingen Info")
        Ppnr.append("Uppgift Saknas")
        Pfnm.append("Uppgift Saknas")
        Ptnm.append("Uppgift Saknas")
        Penm.append("Uppgift Saknas")
        Padd.append("Uppgift Saknas")
        Port.append("Uppgift Saknas")
        Pstnr.append("Uppgift Saknas")
        Plnd.append("Uppgift Saknas")    
        
        
df['Type'] = Type


dfprs=df[df['Type'].isin(['Person', 'Ingen Info'])]  
dforg=df.loc[df['Type'] == "Organisation"]
dftx=df.loc[df['Type'] == "Endast_Taxsuppgift"]

dfprs["Personnummer"] = Ppnr
dfprs["Fornamn"] = Pfnm
dfprs["Tilltalsnamn"] = Ptnm
dfprs["Efternamn"] = Penm
dfprs["Adress"] = Padd
dfprs["PostNr"] = Pstnr
dfprs["Postort"] = Port
dfprs["Land"] = Plnd

dforg["OrgNamn"]=Oonm 
dforg["OrgNr"]=Oonr 
dforg["PostOrt"]=Opos 
dforg["PostNr"]=Opnr
dforg["JurdiskForm"]=Ojrf
dforg["Adress"]=Oadr 

dftx['TaxInfo'] = Txlist

for kol in dfprs.columns:
    dfprs['{}'.format(kol)].replace(r'(Personnummer:|Postort:|Postnummer:|F\xf6rnamn:|Adress:|Tilltalsnamn:|Efternamn:|Land:)', "", regex=True, inplace=True)

for kol in dforg.columns:
    dforg['{}'.format(kol)].replace(r'(Organisationsnummer:|Postort:|Postnummer:|Juridisk form:|Adress:|Organisationsnamn:)', "", regex=True, inplace=True)

perList=['FASTIGHET', 'Personnummer', 'Fornamn', 'Tilltalsnamn', 'Efternamn', 'KOMMUNNAMN', 'TRAKT', 'Adress', 'PostNr', 'Postort', 'Land', 'AREA_HA', 'EXTERNID', 'EXLINK']      
orgList = ['FASTIGHET','OrgNamn','OrgNr','KOMMUNNAMN','TRAKT','Adress','PostNr', 'PostOrt', 'JurdiskForm','AREA_HA','EXTERNID','EXLINK']
txList = ['FASTIGHET', 'KOMMUNNAMN','TRAKT', 'EXTERNID','EXLINK', 'TaxInfo']

dfprs=dfprs[perList]
dforg=dforg[orgList]
dftx=dftx[txList]

dfprs.rename(columns={'FASTIGHET':'Fastighet', 'KOMMUNNAMN':'Kommunnamn', 'TRAKT':'Trakt'}, inplace=True)
dforg.rename(columns={'FASTIGHET':'Fastighet', 'KOMMUNNAMN':'Kommunnamn', 'TRAKT':'Trakt'}, inplace=True)
dftx.rename(columns={'FASTIGHET':'Fastighet', 'KOMMUNNAMN':'Kommunnamn', 'TRAKT':'Trakt'}, inplace=True)

path=os.chdir()
print "Files are at: "+path
    
dforg.to_csv("OrgLista.txt", sep=',', encoding="windows-1252", index=False)
dfprs.to_csv("PersLista.txt", sep=',', encoding="windows-1252", index=False)
dftx.to_csv("TaxeringLista.txt", sep=',', encoding="windows-1252", index=False)
