import requests
import time
from bs4 import BeautifulSoup
import json
import urllib.request 
import timeit
import os
from datetime import datetime
from pathlib import Path
import json



def startScrap(url):
    filePodcastName = "Darknet.Diaries"

    folderName = os.path.dirname(__file__) + "\\output\\" + filePodcastName 
    print("Initial Folder Name: " + folderName)
    if os.path.exists(folderName):
        print("Folder found!")
    else:
        os.mkdir(folderName)
        print("Folder not found! Folder created")
        
    print("URL : " + url)
    mainRes = requests.get(url)

    soup = BeautifulSoup(mainRes.content, 'html.parser')


    contents = soup.find_all(class_="post__content")
    for content in contents:



        aTag = content.find("a")
        
        print(f'Episode URL : https://darknetdiaries.com{aTag["href"]}')
        episodeRes = requests.get(f'https://darknetdiaries.com{aTag["href"]}')
        soupRes = BeautifulSoup(episodeRes.content, 'lxml')

        obj = soupRes.select_one('.single-post').find('script').text.replace("window.playerConfiguration =", "")
        jsonObj = json.loads(obj)
        mp3Url = jsonObj["episode"]["media"]["mp3"]
        coverUrl = jsonObj["episode"]["coverUrl"]
        url = jsonObj["episode"]["url"]
        title = jsonObj["episode"]["title"]
        episodeNumber = aTag["href"].split("/")[2]
        description = soupRes.select_one('.single-post').text.strip()
        
        dateContainer = soupRes.select_one('.hero--single')
        dateUplaoded = dateContainer.find("p").text.split("|")[0].strip()
        formatDate = datetime.strptime(dateUplaoded, '%d %B %Y')
        date = str(formatDate.day) +"."+ str(formatDate.month) +"."+ str(formatDate.year)

        folderName = os.path.dirname(__file__) + "\\output\\" + filePodcastName  + "\\" + episodeNumber + "-" + date

        # make folder name eg. B:\workspace\mcflurry\podcast-tracker\Darknet.Diaries\131-27.12.2022\
        print("Folder Name: " + folderName)
        if os.path.exists(folderName):
            print("Folder found!")
        else:
            os.mkdir(folderName)
            print("Folder not found! Folder created")

        # save file into B:\workspace\mcflurry\podcast-tracker\Darknet.Diaries\131-27.12.2022\data.json
        data = {
            "coverUrl": coverUrl,
            "mp3Url": mp3Url,
            "url": url,
            "title": title,
            "dateUplaoded":date,
            "description":description
        }

        with open(folderName + "\\" + "data.json", "w") as outfile:
            json.dump(data, outfile)
            
        # save mp3
        urllib.request.urlretrieve(mp3Url , folderName+"/"+ episodeNumber + ".mp3") # save file to B:\workspace\mcflurry\podcast-tracker\Darknet.Diaries\128-15.11.2022\128.mp3


    # Next page
    paginationContainer = soup.find("section", {"class": "pagination"}).find_all("div", attrs={"class":"column"})
    if (paginationContainer[2].find("a")):
        # IF next button exist
        startScrap("https://darknetdiaries.com"+paginationContainer[2].find("a")["href"])

        

if __name__ == '__main__':
    startScrap("https://darknetdiaries.com/episode")

