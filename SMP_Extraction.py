# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 10:34:56 2019
@author: MartinTropse
"""

from selenium.webdriver.support.select import Select
from selenium import webdriver
import re
import time
from selenium.webdriver.chrome.options import Options
import os 
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import tabula
import pytesseract
from PIL import Image
from wand.image import Image as wi
import io

"""
Download data (pdf and txt) from the SMP database. The data is divided by municipality
and year. This script is connected to a second script that data mines and summarize the 
data.  

Additional development:
Develop as a part of a GUI?
Further error search 
"""
# =============================================================================
# Function to export all pdfs and emissionsreports from the SMP database.  
# This is then divided by municipality and year
# =============================================================================
mail="joakim.a.svensson@lansstyrelsen.se"
url = "https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx"
password = ""
kommunList = ["Boxholm", "Finspång", "Kinda"] #"Linköping","Mjölby","Motala","Norrköping", "Söderköping","Vadstena", "Valdemarsvik", "Ydre", "Åtvidaberg", "Ödeshög"


def DownloadSMP(muni, year="2018"):
    muniPath="C:\SMP\\"+year+"\\"+muni
    os.makedirs(muniPath, exist_ok=True)
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs", {"download.default_directory":muniPath})
    browser=webdriver.Chrome(executable_path="C:/Py3/chromedriver.exe", options=chromeOptions)
    browser.get(url)
    elemMail=browser.find_element_by_id("PageContent_ucLogin_txtUsername")
    elemMail.send_keys(mail)
    elemPass=browser.find_element_by_id("PageContent_ucLogin_txtPassword")
    elemPass.send_keys(password)
    logButton=browser.find_element_by_name("ctl00$PageContent$ucLogin$btnLogin")
    logButton.click()
    lanElem=browser.find_element_by_id("_Miljörapport")
    lanElem.click()
    while True:
        try:
            obj = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlLan'))
            obj.select_by_value("05")
        except StaleElementReferenceException:
            continue
        break
    while True:
        try:
            objKom = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlKommun'))
        except StaleElementReferenceException:
            continue
        break
    time.sleep(1)
    objKom.select_by_visible_text(muni)
    while True:
        try:
            objYear = Select(browser.find_element_by_id("PageContent_ucSearchAnlaggning_ddlVerksamhetsAr"))
            objYear.select_by_visible_text(year) #Value: 112 Linköping kommun. 134 LstE 
            objMynd = Select(browser.find_element_by_id("PageContent_ucSearchAnlaggning_ddlTillsynsmyndighet"))
            objMynd.select_by_index(0) #Value: 112 Linköping kommun. 134 LstE  
            elemShow=browser.find_element_by_id("btnSearch")
            elemShow.click()
        except (StaleElementReferenceException, ElementClickInterceptedException): #
            continue
        break
    while True:
        try:
            uStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassU").is_selected() #Check if the boxes are filled, if not, fill it!
            if not uStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassU").click()
                
            tStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassT").is_selected()
            if not tStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassT").click()
                
            pStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassP").is_selected()
            if not pStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassP").click()
                
            cStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassC").is_selected()
            if not cStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassC").click()
                
        except StaleElementReferenceException:
            continue
        break
    count = 0 
    n = 0
    time.sleep(2)
    d=browser.find_elements_by_class_name('headRow')
    for x in d:
        hit=re.match(r".+\s\d-\d+\s[a-z,A-Z]+\s\d+", x.text) # Matches e.g. Visar 61-72 av 72
        if hit:
            D=hit.group(0).split(" ") #Splites the data by words
    while int(D[-1]) > n: #Takes out the last number of the string ~"Visar 61-72 av 72". n is increased by 30 per step in the loop, since the amount of shown values is 30. When n is bigger then D[-1] loop breaks.  
        n += 30
        elems = browser.find_elements_by_xpath('//a[@href]')
        for elem in elems:
            if elem.text == "Emissonsdeklaration":
                elem.click()
            if elem.text == "nästa >>":
                elem.click()
                time.sleep(5)
                count = 0
                break
            if count == 1:
                elem.click()
                time.sleep(4)
                count = 0
            else:
                 a=re.match(r'\d{6},\s\d{2}:\d{2}\s\(\d\)', elem.text) #Matches e.g. 190711, 14:59 (3)
                 if a:
                    count += 1
    print(f"\nCompleted downloads from {muni} {year}")                

for muni in kommunList:
    DownloadSMP(muni, "2016")
