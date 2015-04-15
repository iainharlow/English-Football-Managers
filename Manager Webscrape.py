
# coding: utf-8

# In[1]:

# Preamble
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from bs4 import BeautifulSoup
import requests, sys, codecs, re

# Make the graphs a bit prettier, and bigger
pd.set_option('display.mpl_style', 'default')

# This is necessary to show lots of columns in pandas 0.12. 
# Not necessary in pandas 0.13.
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)

plt.rcParams['figure.figsize'] = (10, 3)
plt.rcParams['font.family'] = 'sans-serif'

os.chdir("C:\\Users\\Iain\\Google Drive\\GitHub\\English Football Manager List\\English-Football-Managers\\")
# Format for reading files in Windows: df = pd.read_csv('data\\file.csv')


# In[2]:

teampage = "http://www.leaguemanagers.com/managers/?club_id=46478"
r = requests.get(teampage)
data = r.text
soup = BeautifulSoup(data)


# In[3]:

clubnames = [str(x.text) for x in soup.find("select").find_all("option")][1:]
clubids = [str(x["value"]) for x in soup.find("select").find_all("option")][1:]
managerlinks = []
n = 0
m = 0


# In[4]:

for clubid in clubids:
    n = n+1
    teampage = "http://www.leaguemanagers.com/managers/?club_id="+clubid
    r = requests.get(teampage)
    data = r.text
    soup = BeautifulSoup(data)
    for x in soup.find_all("a",href=re.compile("/managers/")):
        managerlinks.append(str(x.get("href")))
    print("Club "+str(n)+" ("+clubnames[n-1]+"): "+str(len(managerlinks)-m)+" managers.")
    m=(len(managerlinks))


# In[5]:

print("Managers = "+str(len(managerlinks)))
unique_managers = list(set(managerlinks))        

# Filter out any that return /managers/x where x is a single letter:
unique_managers = list(filter(lambda x: len(x) > 12,
                              unique_managers))
print("Unique Managers = "+str(len(unique_managers)))


# In[6]:

# Loop across all unique managers who've managed a current league club:
l=len(unique_managers)
num=0
manlist=[]
for man in unique_managers:

    try: 
        # Get and parse manager's profile page:
        manpage = "http://www.leaguemanagers.com"+str(man)
        r = requests.get(manpage)
        data = r.text
        soup = BeautifulSoup(data)
        num = num+1
        if len(str(data)) > 0 and 'Server Error' not in str(soup):
            if len(soup.find_all("div",class_="first-name")) > 0 and len(soup.find_all("div",class_="last-name")) > 0:
                if num % 100 == 0:
                    print(str(num)+' of '+str(l)+' complete')
                fname = str(soup.find_all("div",class_="first-name")[0].text).strip()
                sname = str(soup.find_all("div",class_="last-name")[0].text).strip()
                name = fname+' '+sname
                cdiv=soup.find_all("div",class_="club")
                sdiv=soup.find_all("div",class_="start-date")
                fdiv=soup.find_all("div",class_="finished-date")

                # Find each appointment and parse club/role/start/end:    
                for i in range(len(cdiv)-1):
                    club = str(cdiv[i+1].find_all("a")[0].text).strip()
                    role = ' '.join(str(cdiv[i+1].text).strip().replace(club,'').split())
                    start = str(sdiv[i+1].text).strip()
                    end = str(fdiv[i].text).strip()
                    # Building the dataset using a list of dictionaries is fast:
                    dict1 = {}
                    dict1.update(url=man,
                                 Name=name,
                                 Club=club,
                                 Role=role,
                                 Start=start,
                                 End=end) 
                    manlist.append(dict1)
            else:
                print('Error: No Name. ',str(num+1),' ',man) # Error to return when link doesn't return a manager page
        else:
            print('Error: Server Error. ',str(num+1),' ',man) # Error to return when link returns nothing
    except:
        #e = sys.exc_info()[0]  #Get exception info (optional)
        print('Error: Incomplete Read. ',str(num+1),' ',man) # Error to return on encoding chunk issue; check requests is updated
        continue
# Convert dataset into a pandas data frame:
mantable = pd.DataFrame(manlist,columns=['url','Name','Club','Role','Start','End'])


# In[10]:

mantable.to_csv('mantable.csv')

