to﻿
"""
Script that find land owners that have a "markavvattningsföretag" (a legal obligation to maintain ditches) contained within their properties, 
meaning thay they are the single owner. 

This GIS-analysis is then connected to "fastighetsregistret" (a database that connects addresses to properites).  

The output that is extracted from fastighetsregistret is in turn used to scrape hitta.se and ratsit.se for telephone 
numbers to the respective properties. This data is then added to the input data and stored as excel file, 
separating personal/company/tax adress info in respective sheets.  
"""

import time
import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import bs4 as bs
import requests

os.chdir("C:/Py/Sandbox/Kontakt")
df=pd.read_csv("PersLista.txt", sep=',', header=0, encoding="windows-1252")

print("Ange namn för sökning")
runName=input()


## =============================================================================
## Hitta.se section. Person information
## =============================================================================
Who=["Fornamn", "Efternamn","Adress", "Postort"]
dfWho=df[Who]

pUrl=dfWho['Fornamn']+" "+dfWho['Efternamn']+", "+dfWho['Adress']+" "+dfWho['Postort']
browser = webdriver.Chrome('C:/Py/chromedriver.exe')

TelListan = []
c = ""
E=""

for pers in pUrl:
    browser.get("https://www.hitta.se/") #Starts webpage
    searchBar=browser.find_element_by_id('search-input')
    searchBar.send_keys(pers)
    searchBar.send_keys(Keys.ENTER)
    curUrl=browser.current_url
    checkPos=re.search(r's%C3%B6k',curUrl)         
    if not checkPos:
        source = requests.get(curUrl).text
        soup=bs.BeautifulSoup(source, 'html.parser')
        phonediv=soup.find_all('a')
        for x in phonediv:
            out=re.search(r'tel:\+(\d+-\d+\s\d+\s\d+|\d+-\d+\s\d+)', str(x))
            if out:
                c = c+"|"+str(out.group(0))
                time.sleep(0.1)
        if c:
            TelListan.append(c)
            c = ""
        else:
            TelListan.append("|Uppgift Saknas")
    else:
        try:
            elem = browser.find_element_by_id("personResults_1")
            elem.click()
            curUrl=browser.current_url
            source = requests.get(curUrl).text
            soup=bs.BeautifulSoup(source, 'html.parser')
            phonediv=soup.find_all('a')
            for x in phonediv:
                out=re.search(r'tel:\+(\d+-\d+\s\d+\s\d+|\d+-\d+\s\d+)', str(x))
                if out:
                    c = c+"|"+str(out.group(0))
                    time.sleep(0.1)
            if c:
                TelListan.append("|Sannolikt|"+c)
                c = ""
            else:
                TelListan.append("|Uppgift Saknas")
        except Exception as e:
            E=e
            if E:
                TelListan.append("|Uppgift Saknas")

for x in range(0,len(TelListan)):
    TelListan[x]=re.sub(r'tel:\+46', '0',TelListan[x])    
    TelListan[x]=re.sub(r'\s+', '',TelListan[x])

for x in range(0, len(TelListan)):
    TelListan[x]=TelListan[x][1:]
        
df['Telefon'] = TelListan

df.replace(r'Ã„','Ä',regex=True, inplace=True)
df.replace(r'Ã–','Ö',regex=True, inplace=True)
df.replace(r'Ã...','Å',regex=True, inplace=True)
# =============================================================================
# ### Ratsit.se: for companies ###
# =============================================================================
odf=pd.read_csv("OrgLista.txt", sep=',', header=0, encoding='latin-1')
#oUrlList = ['OrgNr', 'PostOrt']
oUrl = odf['OrgNr']

ophoneList = []

for url in oUrl:
    browser.get("https://www.ratsit.se/")
    searchVem=browser.find_element_by_id("vem")
    searchVem.send_keys(url)
    searchVem.send_keys(Keys.ENTER)
    elem=browser.find_element_by_class_name("search-list-content")
    href=elem.get_attribute('href')
    browser.get(href)
    source=requests.get(href).text
    soup = bs.BeautifulSoup(source, 'html.parser')
    time.sleep(0.1)
    aPhone=soup.find('p', id='phone')
    if aPhone:
        bPhone=aPhone.text
        bPhone=re.sub(r'(,\n+|\n+)', ",", bPhone)
        bPhone=bPhone[1:-1]
        bPhone=bPhone.split(',')
        ophoneList.append(bPhone[0])
    else:
        ophoneList.append("UppgiftSaknas")

odf.insert(3, column="Telefon", value=ophoneList)

odf.replace(r'Ã„','Ä',regex=True, inplace=True)
odf.replace(r'Ã–','Ö',regex=True, inplace=True)
odf.replace(r'Ã...','Å',regex=True, inplace=True)

tdf=pd.read_csv("TaxeringLista.txt", sep=',', index_col=0)

os.makedirs(f"C:/Kontakt/{runName}")
os.chdir(f"C:/Kontakt/{runName}")

with pd.ExcelWriter('FastighetAdressSammanställning.xlsx') as writer:  # doctest: +SKIP
    df.to_excel(writer, sheet_name='Person_Adress', index=0)
    odf.to_excel(writer, sheet_name='Organisation_Adress', index=0)
    tdf.to_excel(writer, sheet_name='Taxering|Exkluderarde_Adresser', index=0)

print("\nContact info is stored at: \n"+os.getcwd())
