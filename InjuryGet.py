#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#This updates the injury test file: https://docs.google.com/spreadsheets/d/19lkC0kjt52UhysvWCu17YCz8CzZajQ4FzsZ3L8zeZcc/edit


# In[ ]:


#Packages
#Time
import time
from datetime import datetime, timedelta, timezone
from datetime import date
timestart = datetime.now(timezone(timedelta(hours=-4), 'EST'))
#Pandas
import pandas as pd
#Gspread
import gspread
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials
#Beatiful Soup
from bs4 import BeautifulSoup
import bs4 as bs
#UrlLib
from urllib.request import Request, urlopen
import urllib.request, json 


# In[ ]:


#defining header
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}


# In[ ]:


#Let's get the Slate Data
#Let's Open NBASlateFeedBuild
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope) 
gc = gspread.authorize(credentials)
sheet = gc.open('InjuryTest')
w1 = sheet.worksheet("Control")

nfllink = w1.acell('b1').value
nbalink = w1.acell('b2').value

req = urllib.request.Request(url=nfllink, headers=header)
with urllib.request.urlopen(req) as url:
    datanfl = json.loads(url.read().decode())

    
req = urllib.request.Request(url=nbalink, headers=header)
with urllib.request.urlopen(req) as url:
    datanba = json.loads(url.read().decode())


# In[ ]:


datatable=[] 
for players in datanfl:
    PlayerID = players['PlayerID']
    Player = players['Name']
    Position = players['Position']
    Team = players['Team']
    Inj = players['InjuryBodyPart']
    Injn =players['InjuryNotes']
    InjS =players['InjuryStatus']
    DepthPos = players['DepthPosition']
    DepthOrder = players['DepthOrder']
    DepthCat = players['DepthPositionCategory']
    Inactive = players['DeclaredInactive']
    
    row=[PlayerID,Player,Position,Team,Inj,Injn,InjS,DepthPos,DepthOrder, DepthCat, Inactive]
    datatable.append(row)


# In[ ]:


df=pd.DataFrame(datatable)
df.columns = ["PlayerID","Player","Position","Team","Inj","Inj Notes", "Inj Status" ,"DepthPos","DepthOrder", "DepthCat", "Inactive"]
df


# In[ ]:


datatable=[]

for players in datanba:
    PlayerID = players['PlayerID']
    Player = players['FirstName']+' '+players['LastName']
    Position = players['Position']
    Team = players['Team']
    try:
        Inj = players['InjuryBodyPart']
        Injn =players['InjuryNotes']
        InjS =players['InjuryStatus']
    except:
        Inj = ''
        Injn =''
        InjS =''
        
    DepthPos = players['DepthChartPosition']
    DepthOrder = players['DepthChartOrder']
    if Inj is None:
        blank=''
    else:
        row=[PlayerID,Player,Position,Team,Inj,Injn,InjS,DepthPos,DepthOrder]
        datatable.append(row)


# In[ ]:


df2=pd.DataFrame(datatable)
df2.columns = ["PlayerID","Player","Position","Team","Inj","Inj Notes", "Inj Status" ,"DepthPos","DepthOrder"]
df2


# In[ ]:


#Let's push props
Goal = sheet.worksheet("NFL")
sheet.values_clear("NFL!a1:k1000")
gd.set_with_dataframe(Goal, df, row=1,col=1)
timenow = datetime.now(timezone(timedelta(hours=-4), 'EST'))
w1.update('c1', timenow.strftime("%B %d, %Y %H:%M:%S"))


# In[ ]:


#Let's push props
Goal = sheet.worksheet("NBA")
sheet.values_clear("NBA!a1:z1000")
gd.set_with_dataframe(Goal, df2, row=1,col=1)
timenow = datetime.now(timezone(timedelta(hours=-4), 'EST'))
w1.update('c2', timenow.strftime("%B %d, %Y %H:%M:%S"))


# In[ ]:




