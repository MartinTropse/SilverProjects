
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 07:50:05 2019
@author: BiGtaiL

Drone Summary_Script. 

The script goes through all jpg, .mov, .mp4 files from three drones on 3 HDD and extract information  
and distrubute it to 4 dataframess, that will become 4 updated maps in ArcGIS. The 
script also prepare the information to create and update the filestructur within 
the county board network. 

When information is extracted from all "drone files" additional columns are added 
by formating and loading data from the excel sheet: 
Direction, angle, wgs84, season, link, movie duration, drone type, DiarieNr, Kategory & comment. 
The data is then exported and all .MOV files are converted to .mp4. 
(note that MP4 is raw data from devil wheras mp4 are converted .mov files)

This script is then connected to two additional scripts that 
Further the scripts makes a log of the previous filestructures, fileupdates 
and file conversions that is used in the update process. 
-

V 0.92 
Added the ability to match the specific MP4 file to a specific JGP file 
by giving them the same name in directory. 
"""



import warnings 
warnings.filterwarnings("ignore") 
import subprocess
import re
import time
import pandas as pd
import numpy as np
import os
from datetime import datetime
import shutil
import sys

col = ["Date/Time Original","Absolute Altitude", "Relative Altitude", "Gimbal Roll Degree","Gimbal Yaw Degree","Gimbal Pitch Degree","Flight Roll Degree","Flight Yaw Degree","Flight Pitch Degree","GPS Latitude", "GPS Longitude", "PictureLink", "Kategori", "DiarieNr", "Kommentar"]        
mov_col = ["Media Create Date","Media Duration", "Flight Pitch Degree","Flight Yaw Degree","Flight Roll Degree", "Gimbal Pitch Degree","Gimbal Yaw Degree","Gimbal Roll Degree", "GPS Altitude","GPS Latitude","GPS Longitude", "MovieLink", "Drone", "Kategori", "DiarieNr", "Kommentar"]

picDf=pd.DataFrame(columns=col)
movDf=pd.DataFrame(columns=mov_col)

seperator = ', '
E = ""
exe = "C:/exiftool/exiftool(-k).exe"

Drone = ["Fantom"]
droneBase="C:/Py3/DroneUpdate/"


print("Please provide partion letter of external harddrive: ")
hddPath = input()

print("Is this a new update? y/n")
update=input()
if update == "y":
    print("Please provide update name")
    nUpdateFolder = input()
    os.makedirs("C:/Py3/DroneUpdate/"+nUpdateFolder,exist_ok=True)
elif update == "n":
    print("Please provide current update folder")
    cUpdateFolder= input()
    print("Is this the last hardrive in the update? y/n")    
    last = input()
    if "y" not in last and "n" not in last: 
        print("\nInvalid last update entry. Please provide 'y' or 'n'\n")
        sys.exit()
else:
    print("Please Provide valid entry")
    sys.exit()


#If the partion path is wrong, change it under discmanagement
baseStr = hddPath+":/Drone"

os.chdir(baseStr)
    
movPos = 0
picPos = 0

N=list(range(-24, 24))
NE=list(range(24, 71))
E=list(range(71, 106))
SE=list(range(106, 151))
S=list(range(151, 181))
S2=list(range(-181,-165))
S=S+S2
SW=list(range(-165,-120))
W=list(range(-120, -75))
NW=list(range(-75,-24))

my_dict = dict.fromkeys(N, "N")
my_dict.update(dict.fromkeys(NE, "NE"))
my_dict.update(dict.fromkeys(E, "E"))
my_dict.update(dict.fromkeys(SE, "SE"))
my_dict.update(dict.fromkeys(S, "S"))
my_dict.update(dict.fromkeys(SW, "SW"))
my_dict.update(dict.fromkeys(W, "W"))
my_dict.update(dict.fromkeys(NW, "NW"))

season = {1:"Winter", 2:"Winter", 3:"Spring",4:"Spring",5:"Spring",6:"Summer",7:"Summer",8:"Summer", 9:"Autumn", 10:"Autumn", 11:"Autumn", 12:"Winter"}
direction = {"N":0,"NE":45,"E":90, "SE":135,"S":180,"SW":225,"W":270,"NW":315}

print("1")

# =============================================================================
# Loop through the file tree, extract data from files and sort the information 
# in picture and movie dataframes. 
# =============================================================================
for dirpath, subdir, filnames in os.walk(baseStr):
    if ".xlsx" in str(filnames):
        katgL = []
        diarL = []
        comL = []
        xlPath=(dirpath+"/"+'Ifyllningsformulär.xlsx').replace("\\","/")
        xlFile=pd.read_excel(xlPath)
        katg = [x for x in xlFile['Kategori']]
        strKatg=seperator.join(katg)
        katgL.append(strKatg)
        try:
            if type(xlFile['DiarieNummer'][0]) == str:
                diarL.append(xlFile['DiarieNummer'][0])
            else:
                diarL.append("Tillstånd Saknas")
        except Exception as g:
            print(g, "\n Could not find DiarieNummer")
            time.sleep(3)
        try:
            if type(xlFile['Kommentar'][0]) == str:
                comL.append(xlFile['Kommentar'][0])
            else:
                comL.append("Ingen Info")
        except Exception as h:
            print(h, "Error with comment section")                
    else:
        diarL = []
        comL = []
        katgL = []
        diarL.append("Excelfil Saknas")
        katgL.append("Excelfil Saknas")
        comL.append("Excelfil Saknas")
    for x in filnames:
        path=(dirpath+"/"+x).replace("\\","/")
        if path.endswith(".JPG"):
            thepicList = []
            process = subprocess.Popen([exe,path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            metadata = [[]]        
            for output in process.stdout:
                line = output.strip()
                hit=re.search(r'(GPS Latitude|GPS Longitude|Gimbal Roll Degree|Gimbal Yaw Degree|Gimbal Pitch Degree|Flight Roll Degree|Flight Yaw Degree|Flight Pitch Degree|Absolute Altitude|Relative Altitude|Date/Time Original)+\s+(?!Ref).+', line)
                if hit:
                    metadata[0].append(hit.group(0))
            df=pd.DataFrame(columns=col)
            pathL = [path] 
            df.loc[picPos] = metadata[0]+[path]+katgL+diarL+comL
            picDf=pd.concat([picDf, df], axis=0)
            picPos +=1
        if '.MOV' in x:
            themovList = []
            process = subprocess.Popen([exe,path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            motadata = [[]]        
            for output in process.stdout:
                print(output)
                line = output.strip()
                hit=re.search(r'(GPS Latitude|GPS Longitude|GPS Altitude|Media Duration|Camera Pitch|Camera Yaw|Camera Roll|Pitch|Yaw|Roll|Media Create Date)+\s+(?!Ref|\(err\)).+', line)
                if hit:
                    motadata[0].append(hit.group(0))
            df=pd.DataFrame(columns=mov_col)
            #themovList = [storepath+x]
            df.loc[movPos] = motadata[0]+[path]+Drone+katgL+diarL+comL
            movDf=pd.concat([movDf, df], axis=0)
            movPos +=1

print("2")
# =============================================================================
# Devil_Section
# =============================================================================
pathList = []
pattern=re.compile(r'.+\.MP4')
pattern2=re.compile(r'.+\.JPG')
mp4col = ["GPS Altitude","Gimbal Roll Degree","Gimbal Yaw Degree","Gimbal Pitch Degree","Flight Roll Degree","Flight Yaw Degree","Flight Pitch Degree","GPS Latitude", "GPS Longitude", "Media Create Date","Media Duration", "MovieLink", "Drone", "Kategori", "DiarieNr", "Kommentar"]
mp4df = pd.DataFrame(columns=mp4col)
Drone = ["Devil"]

for dirpath, subpath, filenames in os.walk(baseStr):
    count = 0
    jpgHitList = []
    if ".xlsx" in str(filenames):
        katgL = []
        diarL = []
        comL = []
        xlPath=(dirpath+"/"+'Ifyllningsformulär.xlsx').replace("\\","/")
        xlFile=pd.read_excel(xlPath)
        katg = [x for x in xlFile['Kategori']]
        strKatg=seperator.join(katg)
        katgL.append(strKatg)
        if type(xlFile['DiarieNummer'][0]) == str:
            diarL.append(xlFile['DiarieNummer'][0])
        else:
            diarL.append("Tillstånd Saknas")
        if type(xlFile['Kommentar'][0]) == str:
            comL.append(xlFile['Kommentar'][0])
        else:
            comL.append("Ingen Info")
    else:
        katgL = []
        diarL = []
        diarL.append("Excelfil Saknas")
        katgL.append("Excelfil Saknas")
    if re.match(pattern, str(filenames)) and re.match(pattern2, str(filenames)):
        for file in filenames:
             path=(dirpath.replace("\\","/"))
             if '.JPG' in path+file:
                 while count == 0:
                     process = subprocess.Popen([exe, path+"/"+file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) 
                     count += 1
                     jpgList = [re.search(r'(GPS Longitude|GPS Latitude|Gimbal Roll Degree|Gimbal Yaw Degree|Gimbal Pitch Degree|Flight Roll Degree|Flight Yaw Degree|Flight Pitch Degree|Relative Altitude)\s+(?!Ref).+', output) for output in process.stdout]
                     for z in jpgList:
                         if z:
                             jpgHitList.append(z.group(0))                     
                     for file in filenames:
                         if '.MP4' in path+file:
                             mp4HitList = []
                             process = subprocess.Popen([exe, path+"/"+file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                             mpList = [re.search(r'(File Modification Date/Time|Media Duration).+', output) for output in process.stdout if type(output) == str] 
                             for x in mpList:
                                 if x:
                                     mp4HitList.append(x.group(0))
                             pathList.append(path+"/"+file)
                             df = pd.DataFrame(columns=mp4col)
                             df.loc[movPos] = jpgHitList+mp4HitList+pathList+Drone+katgL+diarL+comL
                             movPos += 1
                             mp4df = pd.concat([df, mp4df], axis = 0)
                             pathList = []

movDf=pd.concat([movDf, mp4df], axis=0, join="outer")    

print("3")

# =============================================================================
# Format the picture df        
# =============================================================================
picDf=picDf.replace(r'^.+:\s', "", regex=True)
picDf=picDf.replace(r' Above Sea Level', "", regex=True)
picDf['GPS Latitude'] = picDf['GPS Latitude'].replace(r'(deg|\')', ".", regex=True) 
picDf['GPS Latitude'] = picDf['GPS Latitude'].replace(r'(\s|" N)', "", regex=True) 
picDf['GPS Longitude'] = picDf['GPS Longitude'].replace(r'(deg|\')', ".", regex=True) 
picDf['GPS Longitude'] = picDf['GPS Longitude'].replace(r'(\s|" E)', "", regex=True)                 


longiList = []
for x in picDf['GPS Longitude']:
    longLista = []
    spltList=x.split(".")
    longLista.append(float(spltList[0])) 
    longLista.append(float(spltList[1])/60)
    longLista.append(float(spltList[2])/3600)
    longLista.append(float(spltList[3])/360000)    
    longiList.append(np.sum(longLista))
picDf['GPS Longitude']=longiList

latiLista = []
for x in picDf['GPS Latitude']:
    latLista = []
    spltList=x.split(".")
    latLista.append(float(spltList[0])) 
    latLista.append(float(spltList[1])/60)
    latLista.append(float(spltList[2])/3600)
    latLista.append(float(spltList[3])/360000)    
    latiLista.append(np.sum(latLista))
picDf['GPS Latitude']=latiLista
       
monthList = []
for x in picDf['Date/Time Original']:
    a=datetime.strptime(x, "%Y:%m:%d %H:%M:%S")
    monthList.append(int(datetime.strftime(a, "%m")))
picDf['Month'] = monthList    
picDf['Season']  = picDf['Month'].map(season) 
picDf['Gimbal Yaw Degree']=picDf['Gimbal Yaw Degree'].astype('float')
picDf['Camera Angle'] = picDf["Gimbal Yaw Degree"].astype('int').map(my_dict)
picDf['NumAngle'] = picDf['Camera Angle'].map(direction)
 
picDf.drop(['Month'], axis=1, inplace=True)
# =============================================================================
# Format the Movie_df 
# =============================================================================
movDf=movDf.replace(r'^.+:\s', "", regex=True)
movDf=movDf.replace(r' Above Sea Level', "", regex=True)
movDf['GPS Latitude'] = movDf['GPS Latitude'].replace(r'(deg|\')', ".", regex=True) 
movDf['GPS Latitude'] = movDf['GPS Latitude'].replace(r'(\s|" N)', "", regex=True) 
movDf['GPS Longitude'] = movDf['GPS Longitude'].replace(r'(deg|\')', ".", regex=True) 
movDf['GPS Longitude'] = movDf['GPS Longitude'].replace(r'(\s|" E)', "", regex=True)                 
movDf['Media Create Date'] = movDf['Media Create Date'].replace(r'\+.+',"", regex=True)
movDf['GPS Altitude'] = movDf['GPS Altitude'].replace(r'(\+|\s|m)',"", regex=True)

longiList = []
for x in movDf['GPS Longitude']:
    longLista = []
    spltList=x.split(".")
    longLista.append(float(spltList[0])) 
    longLista.append(float(spltList[1])/60)
    longLista.append(float(spltList[2])/3600)
    longLista.append(float(spltList[3])/360000)    
    longiList.append(np.sum(longLista))
movDf['GPS Longitude']=longiList

latiLista = []
for x in movDf['GPS Latitude']:
    latLista = []
    spltList=x.split(".")
    latLista.append(float(spltList[0])) 
    latLista.append(float(spltList[1])/60)
    latLista.append(float(spltList[2])/3600)
    latLista.append(float(spltList[3])/360000)    
    latiLista.append(np.sum(latLista))
movDf['GPS Latitude']=latiLista
       
monthList = []
for x in movDf['Media Create Date']:
    a=datetime.strptime(x, "%Y:%m:%d %H:%M:%S")
    monthList.append(int(datetime.strftime(a, "%m")))
movDf['Month'] = monthList    
movDf['Season']  = movDf['Month'].map(season) 
movDf['Gimbal Yaw Degree']=movDf['Gimbal Yaw Degree'].astype('float')
movDf['Camera Angle'] = movDf["Gimbal Yaw Degree"].astype('int').map(my_dict)

movDf['NumAngle'] = movDf['Camera Angle'].map(direction)
movDf.drop('Month', axis=1, inplace=True)
movDf['Media Duration']=movDf['Media Duration'].replace("s","", regex=True)

pattern=re.compile(r'\.\d+')

for dur,aRange in zip(movDf['Media Duration'],range(0,len(movDf['Media Duration']))):
    if '.' in dur:
        dur="0:00:"+str(round(float(dur),2))
        movDf['Media Duration'][aRange]=re.sub(pattern, "", dur)

newCol=['Media Create Date', 'Media Duration', 'Season', 'Kategori', 'Kommentar', 'DiarieNr', 'MovieLink', 'GPS Latitude',
        'GPS Longitude', 'GPS Altitude', 'Camera Angle', 'NumAngle',
        'Drone',  'Flight Pitch Degree', 'Flight Roll Degree', 'Flight Yaw Degree',
        'Gimbal Pitch Degree', 'Gimbal Roll Degree', 'Gimbal Yaw Degree']
movDf = movDf[newCol]

newpiCol = ['Date/Time Original', 'Camera Angle', 'Season', 'Kategori', 'Kommentar', 'DiarieNr','PictureLink','GPS Latitude', 
            'GPS Longitude', 'Absolute Altitude',  'Relative Altitude', 'NumAngle', 
            'Gimbal Roll Degree', 'Gimbal Yaw Degree', 'Gimbal Pitch Degree', 
            'Flight Roll Degree', 'Flight Yaw Degree', 'Flight Pitch Degree']
picDf = picDf[newpiCol]


        
# =============================================================================
# Go through folder tree and convert all .MOV files to mp4 
# =============================================================================
_MOV_l= []

dfMOV=pd.read_csv(hddPath+":/MOV_Backup/Converted_MOV.csv", encoding="windows-1252")


sap = ""
mov_list = []

for mfile in dfMOV['MOV_Files']:
    mfile=list(mfile)
    mfile[0] = hddPath
    a=sap.join(mfile)
    mov_list.append(a)

dfMOV['MOV_Files'] = mov_list

for dirpath, dirnames, filenames in os.walk(baseStr):
      for x in filenames: 
          if x.endswith(".MOV"):
              temp=dirpath.replace("\\", "/")
              file=os.path.join(temp+"/"+x)        
              out=file[:-4]+".mp4"
              if file not in list(dfMOV.MOV_Files):
                  print(f"Converting {x}....")
                  p1=subprocess.run(['ffmpeg.exe', '-i', file, out], capture_output=True, text=True)
                  pos=len(dfMOV.MOV_Files)+1
                  dfMOV.loc[pos] = file
                  
dfMOV.to_csv(hddPath+":/MOV_Backup/Converted_MOV.csv", encoding="windows-1252", index=False)          
# =============================================================================
# Change links path to movie and pictures        
# =============================================================================
movDf["MovieLink"] = movDf["MovieLink"].replace(".MOV", ".mp4", regex=True)
             
# =============================================================================
# Check for new files compared to previous update and create folders/files with info
# =============================================================================
newCopy=pd.DataFrame()
updateHist=pd.read_csv(hddPath+":/LastUpdate/updateHistory.csv", encoding="windows-1252", sep=',')

upList = []

for file in updateHist['Files']:
    life=list(file)
    life[0] = hddPath
    alife = "".join(life)
    upList.append(alife)

updateHist['Files']=upList


newCopy['Files'] = picDf['PictureLink'].append(movDf['MovieLink'])
newCopy['Files']=newCopy['Files'].replace(".MOV", ".mp4", regex=True)

if len(os.listdir(hddPath+":/LastUpdate")) == 1:
    newCopy.to_csv(hddPath+":/LastUpdate/lastCopy.csv", sep=',', encoding="windows-1252", index=False)
    newCopy.to_csv(hddPath+":/LastUpdate/changes_last_update.csv", header=1, encoding="windows-1252", sep=',', index=False)
    updateDf=pd.concat([newCopy, updateHist], axis=0)
    updateDf.to_csv(hddPath+":/LastUpdate/updateHistory.csv", encoding="windows-1252", sep=',', index=False) 
    print("Update data is stored at: "+hddPath+":/LastUpdate")        
else:
    changeL = []
    changeFrame = pd.DataFrame()
    for path in list(newCopy['Files']):
        if path not in list(updateHist['Files']):
            changeL.append(path)    
    changeFrame['Files'] = changeL
    if len(changeFrame['Files']) !=0:
        changeFrame.to_csv(hddPath+":/LastUpdate/changes_last_update.csv", header=1, encoding="windows-1252", sep=',', index=False)        
        timeStamp=time.localtime()
        datum = time.strftime("%Y%m%d-%H%M")
        os.mkdir(f"{hddPath}:/LastUpdate/Update {datum}")
        shutil.copyfile(hddPath+":/LastUpdate/changes_last_update.csv", f"{hddPath}:/LastUpdate/Update {datum}/lastCopy.csv")
        pd.concat([changeFrame, updateHist], axis=0).to_csv(hddPath+":/LastUpdate/updateHistory.csv", encoding="windows-1252", sep=',', index=False)
        print(f"Update data is stored at: {hddPath}:\LastUpdate")
    else:
        print("No changes were made since last run")
        updateHist.to_csv(hddPath+":/LastUpdate/updateHistory.csv", encoding="windows-1252", sep=',', index=False)
        changeFrame.to_csv(hddPath+":/LastUpdate/changes_last_update.csv", header=1, encoding="windows-1252", sep=',', index=False)

movDf["MovieLink"] = movDf["MovieLink"].replace(hddPath+":/Drone/", "T:/Rasterdata/E/Drone/", regex=True)
picDf['PictureLink'] = picDf['PictureLink'].replace(hddPath+":/Drone/", "T:/Rasterdata/E/Drone/", regex=True)

# =============================================================================
# Concat and store map output
# =============================================================================
#Is this a new update: 
if update == "y":
    print("\nCreating new mapfiles")
    picDf.to_csv(droneBase+nUpdateFolder+"/DronePictureData.csv", sep=',', encoding="windows-1252", index=False)     
    movDf.to_csv(droneBase+nUpdateFolder+"/DroneMovieData.csv", sep=',', encoding="windows-1252", index=False)

if update == "n":
    print("\nUpdating map info")
    updatePDF=pd.read_csv(droneBase+cUpdateFolder+"/DronePictureData.csv", sep=',', encoding="windows-1252")
    updateMDF=pd.read_csv(droneBase+cUpdateFolder+"/DroneMovieData.csv", sep=',', encoding="windows-1252")
    newPDF=pd.concat([updatePDF, picDf], axis=0)
    newMDF=pd.concat([updateMDF, movDf], axis=0)
    if last == "n":
        newPDF.to_csv(droneBase+cUpdateFolder+"/DronePictureData.csv", sep=',', encoding="windows-1252", index=False)
        newMDF.to_csv(droneBase+cUpdateFolder+"/DroneMovieData.csv", sep=',', encoding="windows-1252", index=False)
    elif last == "y":
        time.sleep(2)
        stopPic = pd.DataFrame(columns=newpiCol)
        permPic = pd.DataFrame(columns=newpiCol)
        permMov = pd.DataFrame(columns=newCol)
        stopMov = pd.DataFrame(columns=newCol)
        pmCounter = 0
        smCounter = 0
        ppCounter = 0
        spCounter = 0
        for row, pos in zip(movDf['DiarieNr'],range(0, movDf.shape[0])):
            if 'Tillstånd Saknas' in row or 'Excelfil Saknas' in row:
                stopMov.loc[smCounter] = movDf.iloc[pos, :]
                smCounter += 1
            else:
                permMov.loc[pmCounter] = movDf.iloc[pos, :]
                pmCounter += 1
        for rowp, posp in zip(picDf['DiarieNr'],range(0, picDf.shape[0])):
            if 'Tillstånd Saknas' in rowp or 'Excelfil Saknas' in rowp:
                time.sleep(1)
                stopPic.loc[spCounter] = picDf.iloc[posp, :]
                spCounter += 1
            else:
                permPic.loc[ppCounter] = picDf.iloc[posp, :]
                ppCounter += 1
        stopPic.to_csv(droneBase+cUpdateFolder+"/DroneStPictureData.csv", sep=',', encoding="windows-1252", index=False)
        permPic.to_csv(droneBase+cUpdateFolder+"/DronePmPictureData.csv", sep=',', encoding="windows-1252", index=False)
        stopMov.to_csv(droneBase+cUpdateFolder+"/DroneStMovieData.csv", sep=',', encoding="windows-1252", index=False)
        permMov.to_csv(droneBase+cUpdateFolder+"/DronePmMovieData.csv", sep=',', encoding="windows-1252", index=False)

print(f"Arcmap data is stored at: {droneBase}")