import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import urllib.request 
import timeit
import os
from datetime import datetime



def startScrap(url):
    podcastTitle = "Darknet.Diaries"

    print(url)
    mainRes = requests.get(url)

    soup = BeautifulSoup(mainRes.content, 'html.parser')

    contents = soup.find_all(class_="post__content")
    for content in contents:



        aTag = content.find("a")
        print(aTag["href"])
        
        print(f'https://darknetdiaries.com{aTag["href"]}')
        episodeRes = requests.get(f'https://darknetdiaries.com{aTag["href"]}')
        soupRes = BeautifulSoup(episodeRes.content, 'lxml')

        obj = soupRes.select_one('.single-post').find('script').text.replace("window.playerConfiguration =", "")
        jsonObj = json.loads(obj)
        mp3Url = jsonObj["episode"]["media"]["mp3"]
        coverUrl = jsonObj["episode"]["coverUrl"]
        url = jsonObj["episode"]["url"]
        title = jsonObj["episode"]["title"]

        
        dateContainer = soupRes.select_one('.hero--single')
        dateUplaoded = dateContainer.find("p").text.split("|")[0].strip()
        formatDate = datetime.strptime(dateUplaoded, '%d %B %Y')
        date = str(formatDate.day) +"."+ str(formatDate.month) +"."+ str(formatDate.year)

        folderName = aTag["href"].split("/")[2] + "-" + date
        fileName = folderName +".mp3"
        
        if os.path.exists(folderName):
            print("Folder found!")
        else:
            os.mkdir(folderName)
            print("Folder not found! Folder created")

        urllib.request.urlretrieve(mp3Url , folderName+"/"+ fileName)
        # start = timeit.default_timer()
        # stop = timeit.default_timer()
        # print('Time: ', stop - start)



    # Next page
    paginationContainer = soup.find("section", {"class": "pagination"}).find_all("div", attrs={"class":"column"})
    if (paginationContainer[2].find("a")):
        # IF next button exist
        startScrap("https://darknetdiaries.com"+paginationContainer[2].find("a")["href"])

        

if __name__ == '__main__':
    startScrap("https://darknetdiaries.com/episode")




# class DarknetDiaries: 
#     def __init__(self, title, date, episode, image, description, ):

