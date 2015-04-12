#Manager_Webscrape.py fetches manager appointment and sacking dates from
# the LMA, leaguemanagers.com.

from bs4 import BeautifulSoup
import requests, sys, codecs, csv, re

#for clubid in range(1,92):

teampage = "http://www.leaguemanagers.com/managers/managers.html?clubid=1"#+clubid
r = requests.get(teampage)
data = r.text
soup = BeautifulSoup(data)

clubnames = [str(x.text) for x in soup.find("select").find_all("option")]
clubids = [str(x["value"]) for x in soup.find("select").find_all("option")]
managerlinks = []
n = 0
m = 0

for clubid in clubids:
    n = n+1
    teampage = "http://www.leaguemanagers.com/managers/managers.html?clubid="+clubid
    r = requests.get(teampage)
    data = r.text
    soup = BeautifulSoup(data)
    for x in soup.find_all("a",href=re.compile("profile")):
        managerlinks.append(str(x.get("href")))
    print("Club "+str(n)+" ("+clubnames[n-1]+"): "+str(len(managerlinks)-m)+" managers.")
    m=(len(managerlinks))

print("Managers = "+str(len(managerlinks)))
unique_managers = list(set(managerlinks))        
print("Unique Managers = "+str(len(unique_managers)))


managertable=[]
    
n = 0
for man in unique_managers:
    man = man.replace("profile","history")
    man = man.replace("manager","managers")
    manpage = "http://www.leaguemanagers.com"+man
    r = requests.get(manpage)
    data = r.text
    soup = BeautifulSoup(data)
    name = str(soup.find_all("td",align="left")[1].text).strip()
    i=0
    x=soup.find_all("td",class_="historyTable")
    for i in range(int(len(x)/5)):
        clubrole = str(x[i*5].text)
        strtdate = str(x[i*5+1].text)
        enddate = str(x[i*5+2].text)
        managertable.append(man+","+name+","+clubrole+","+strtdate+","+enddate)
    n = n+1
    if n % 10 == 0:
        print(str(n)+" of "+str(len(unique_managers))+" completed.")

print(len(managertable))

#Write data to | separated CSV files:    
manfile = "Managers2.csv"
file = open(manfile, "w", newline="",encoding="latin-1")   
file.writelines( "%s\n" % item for item in managertable )
file.close()
    