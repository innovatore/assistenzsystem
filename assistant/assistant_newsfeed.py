# -*- coding: UTF-8 -*-

import assistant_soundprocess
import feedparser, re
from time import *
from random import seed
from random import choice

masterVolume = '100'
voiceVolume = '100'
startupSound = '/home/pi/Desktop/startup.wav'
gong = '/home/pi/Desktop/Atone.wav'
blib = '/home/pi/Desktop/blib.wav'
beep = '/home/pi/Desktop/beep.mp3'
newsId = 0
cancelNews = False
seed()

def PlayNews(g, l, t):
    global cancelNews
    if assistant_soundprocess.IsSoundProcessActive() == False:
        cancelNews = False
        
    if cancelNews == True:
        cancelNews = False
        assistant_soundprocess.CreateSoundProcessMPG123(beep, 100)
        sleep(0.5)
        assistant_soundprocess.CleanUpSoundProcessList()
    else:
        cancelNews = True
        global newsId
        global newsList 
        assistant_soundprocess.CleanUpSoundProcessList()
        if newsList != 0:
            if (newsId == len(newsList)):
                newsList = 0
                newsId = 0
#        PlayRSS(newsId)
        PlayRandomRSS()
        newsId = newsId + 1
        

def PlayRSS(newsId):
    assistant_soundprocess.CreateSoundProcessAplay(gong, voiceVolume)
    global newsList
    if newsList == 0:
        newsList = LoadRSS("SPIEGEL")
        newsList.entries.append(LoadRSS("Bischof Bode").entries)
        newsList.entries.append(LoadRSS("STERN").entries)
        newsList.entries.append(LoadRSS("Boulevard").entries)
        if newsList == 0:
            return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut("Es konnten keine Nachrichten gefunden werden."), voiceVolume)
    if newsList != 0:
        PlayNewsListItemById(newsId)
        
def PlayRandomRSS():
    assistant_soundprocess.CreateSoundProcessAplay(gong, voiceVolume)
    global newsList
    if newsList == 0:
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut("Es konnten keine Nachrichten gefunden werden."), voiceVolume)
    else:
        PlayNewsListItem(choice(newsList.entries))
        
def PlayNewsListItem(newsItem):
    try:
        outputstr = newsItem.title + ": " + newsItem.description
#            outputstr = newsItem.title + ": " + newsItem.summary
        outputstr = re.sub("<.*?>", "", outputstr)
        outputstr = outputstr.replace("'", "")
#            outputstr = outputstr.encode('utf-8')
#           outputstr = outputstr.replace('\xc3', '')
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), voiceVolume)
    except KeyError:
        outputstr = "Encoding fehlgeschlagen!"
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), voiceVolume)

        
def PlayNewsListItemById(newsId):
    print (newsId)
    print (" : ")
#       print (newsList.entries)
    post = newsList.entries[newsId]
    print (post)

    try:
        outputstr = post.title + ": " + post.description
#            outputstr = post.title + ": " + post.summary
        outputstr = re.sub("<.*?>", "", outputstr)
        outputstr = outputstr.replace("'", "")
#            outputstr = outputstr.encode('utf-8')
#           outputstr = outputstr.replace('\xc3', '')
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), voiceVolume)
    except KeyError:
        outputstr = "Encoding fehlgeschlagen!"
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), voiceVolume)


def LoadRSS(provider):
    if provider == "Bischof Bode":
        feedUrl = 'https://bistum-osnabrueck.de/author/bischof/feed'
    elif provider == "Boulevard":
        feedUrl = 'http://www.naanoo.com/live/feed'
    elif provider == "STERN":
        feedUrl = 'http://www.stern.de/feed/standard/all'
    elif provider == "SPIEGEL":
        feedUrl = 'http://www.spiegel.de/schlagzeilen/tops/index.rss'
    try:
        feedData = feedparser.parse(feedUrl)
        outputstr = "Es wurden " + str(len(feedData)) + " Schlagzeilen von " + provider + " abgerufen."
#           outputstr = feedData['feed']['title'] + " Abgerufen am " + strftime("%d.%m.%Y um %X ", localtime()) + " "
    except KeyError:
#           outputstr = "Laden der Daten von Spiegel.de fehlgeschlagen!"
        outputstr = "Kein Netzwerk zum Laden der Schlagzeilen."
        feedData = 0
    if str(feedData).find("bozo_exception") > 0:
#           outputstr = "Laden der Daten von Spiegel.de fehlgeschlagen!"
        outputstr = "Kein Netzwerk zum Laden der Schlagzeilen."
        feedData = 0
    if feedData != 0:
        for index in range(len(feedData.entries)):
            feedData.entries[index].title = provider + " schreibt: " + feedData.entries[index].title
    assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), voiceVolume)
    sleep(2)
    return feedData