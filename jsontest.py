#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:30:12 2019

@author: ericalvarado
"""

import json
import urllib.request
from bs4 import BeautifulSoup
import csv
import datetime

def scrapeKS(url):
    res  = urllib.request.urlopen(url)  # response object
    html = res.read()
    soup = BeautifulSoup(html,"html5lib")
    
    #fullDesc = soup.findAll('div', attrs={'class':'full-description js-full-description responsive-media formatted-lists'})
    
    imgCount = soup.findAll('img', attrs={'class':'fit'})
    
    embedCount = soup.findAll('div', attrs={'class':'template oembed'})
    
    pCount = soup.findAll('p')
    
    pageContent = []
    for items in pCount:
        numberOfItems = len(items.contents)
        for i in range(numberOfItems):
            pageContent.append(items.contents[i])
    
    wordCount = 0
    for line in pageContent:
        temp = str(line).split()
        wordCount = len(temp) + wordCount
    
    
    #print (len(fullDesc))
    #print("URL: {}".format(url))
    #print("Number of Images: {}".format(len(imgCount)))
    #print("Number of Videos: {}".format(len(embedCount)))
    #print("Number of Paragraph Sections: {}".format(len(pCount)))
    #print("Number of Words: {}".format(wordCount))
    return(len(imgCount),len(embedCount),len(pCount),wordCount)

def writeDictToCSV(gameList):
    #### Write list of dictionary items to CSV file ####  
    print("#### writeDictToCSV Function Initiated #####")        
    outputFileName = path + "outputfile_{}.csv".format(datetime.datetime.now().strftime("%I%M%S"))
    
    with open(outputFileName, 'w', newline='') as csvfile:
        fieldnames = ['category','name','country','currency','goal','backerCount','pledgedAmount','usdPledged',
                  'launchedAt','deadline','state','stateChangedAt','url','spotlight','staffPick','imgCount',
                  'embedCount','pCount','wordCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
    
        for dictItem in gameList:
            writer.writerow(dictItem) 
    return True

#file = "Kickstarter_2019-03-14T03_20_12_200Z.json"
file = "Kickstarter_2019-02-14T03_20_04_734Z.json"
path = "/Users/ericalvarado/Dropbox/CUS615 - Data Mining 2/Project/JSON Data/"

 #### Walk the data file, strip out pertinent properties, and write games category to list
print("#### walkDataFile Function Initiated #####")            
with open(path+file, 'r') as f:
    data = [json.loads(line) for line in f]
nonGameList = []
gameList = [] 

print('#### starting JSON walk ####')
for i in range(len(data)):
    print(i)
    tempDict = {}
    for k, v in data[i]['data'].items():
        #print(k,v)
        if k == 'category':
            tempDict["category"]=v['id']
        if k == 'name':
            tempDict["name"] = v.replace(","," ")
        if k == 'country':
            tempDict['country'] = v.replace(","," ")
        if k == 'currency':
            tempDict['currency'] = v.replace(","," ")
        if k == 'goal':
            tempDict['goal'] = v
        if k == 'backers_count':
            tempDict['backerCount'] = v
        if k == 'converted_pledged_amount':
            tempDict['pledgedAmount'] = v
        if k == 'usd_pledged':
            tempDict['usdPledged'] = v
        if k == 'launched_at':
            tempDict['launchedAt'] = v
        if k == 'deadline':
            tempDict['deadline'] = v
        if k == 'state':
            tempDict['state'] = v
        if k == 'state_changed_at':
            tempDict['stateChangedAt'] = v
        if k == 'urls':
            tempDict['url'] = v['web']['project']
        if k == 'spotlight':
            tempDict['spotlight'] = v
        if k == 'staff_pick':
            tempDict['staffPick'] = v
    #print(tempDict)
    if tempDict["category"]==34:
        #print(tempDict['url'])
        tempTuple = scrapeKS(tempDict['url'])
        tempDict["imgCount"] = tempTuple[0]
        tempDict['embedCount'] = tempTuple[1]
        tempDict['pCount'] = tempTuple[2]
        tempDict['wordCount'] = tempTuple[3]
        gameList.append(tempDict)
#    else:
#        nonGameList.append(tempDict)
               
writeDictToCSV(gameList)

      

# Reference
# https://docs.python.org/2/library/datetime.html#datetime-objects
# https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
# https://pythonspot.com/http-parse-html-and-xhtml/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
# https://docs.python.org/3.0/library/urllib.request.html
# https://stackoverflow.com/questions/2136267/beautiful-soup-and-extracting-a-div-and-its-contents-by-id
# https://www.enigmeta.com/blog/counting-words-with-python-3/
# https://linuxconfig.org/how-to-parse-data-from-json-into-python
