#!/usr/bin/python

import assistant_soundprocess
import os
from time import *
from random import seed
from random import choice

masterVolume = '80'
voiceVolume = '100'
startupSound = '/home/pi/Desktop/startup.wav'
gong = '/home/pi/Desktop/Atone.wav'
blib = '/home/pi/Desktop/blib.wav'
beep = '/home/pi/Desktop/beep.mp3'
songId = 0
cancelSong = False
songCount = 0
seed()

def PlayGong(g, l, t):
  return assistant_soundprocess.CreateSoundProcessAplay(gong, voiceVolume)

def PlayError(g, l, t):
    return assistant_soundprocess.CreateSoundProcessAplay(blib, masterVolume)

def PlayBeep(g, l, t):
    return assistant_soundprocess.CreateSoundProcessMPG123(beep, masterVolume)

def SaySomething(g, l, t):
    return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut("Hallo"), masterVolume)

def PlaySong(g, l, t):
    global cancelSong
    if assistant_soundprocess.IsSoundProcessActive() == False:
        cancelSong = False
        
    if cancelSong == True:
        cancelSong = False
        PlayBeep(1,2,3)
        sleep(0.5)
        assistant_soundprocess.CleanUpSoundProcessList()
    else:
        cancelSong = True
        global songId
        global songCount
        assistant_soundprocess.CleanUpSoundProcessList()
#        PlayMusic(songId)
#        songId = songId + 1
        PlayMusicRandomly()


def GetSongNameList(location):
    songNames = []
    for (filenames) in os.walk(location):
        songNames.extend(filenames)
        break
    songNames = songNames[2]
    return songNames

def CreateMusicPlayList():
    global songCount
    musicLocation = '/home/pi/Music/omamp3/'
    songNames = GetSongNameList(musicLocation)
    songCount = len(songNames)
    message = "Es wurden "
    message += str(songCount)
    message += "Lieder geladen "
    message += "Bitte warten"
    assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(message), voiceVolume)
    sleep(2)
    return songNames

def PlayMusic(songId):
    print ("PlayMusic")
    musicLocation = '/home/pi/Music/omamp3/'
    global musicPlayList
    soundProcessPID = assistant_soundprocess.CreateSoundProcessAplay(gong, masterVolume)
    sleep(0.5)
    soundProcessPID = assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut("Ich spiele jetzt: " + musicPlayList[songId].split('.')[0]), voiceVolume)
    sleep(2)
    return assistant_soundprocess.CreateSoundProcessMPG123(musicLocation + musicPlayList[songId], masterVolume)

def PlayMusicRandomly():
    print ("PlayMusic")
    musicLocation = '/home/pi/Music/omamp3/'
    global musicPlayList
    soundProcessPID = assistant_soundprocess.CreateSoundProcessAplay(gong, masterVolume)
    sleep(0.5)
    tuneToPlay = choice(musicPlayList)
    soundProcessPID = assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut("Ich spiele jetzt: " + tuneToPlay.split('.')[0]), voiceVolume)
    sleep(2)
    return assistant_soundprocess.CreateSoundProcessMPG123(musicLocation + tuneToPlay, masterVolume)

def PlayWaitMusic():
    print("PlayWaitMusic")
#    waitMusic = '/home/pi/Music/Elevator Music.mp3'
    waitMusic = '/home/pi/Music/ps4 main.mp3'
#    waitMusic = '/home/pi/Music/Nintendo 3DS.mp3'
    return assistant_soundprocess.CreateSoundProcessMPG123ForWait(waitMusic, 18)

def SilenceSounds():
    assistant_soundprocess.CleanUpSoundProcessList()

def SaySomething(text):
    return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(text), masterVolume)