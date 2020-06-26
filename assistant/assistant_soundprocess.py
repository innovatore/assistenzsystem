# -*- coding: UTF-8 -*-
import datetime, os, subprocess, sys, psutil

soundProcessList = []
soundProcessListWav = []
soundProcessListLocations = []
soundProcesses = []



###############################################################################################

def CreateSoundProcessAplay(fileLocation, volume):
    print ("CreateSoundProcess ")
    print (fileLocation)
    global soundProcessList
    global soundProcessListLocations
    global soundProcesses
    soundProcess =  subprocess.Popen(["aplay", fileLocation], stdin=subprocess.PIPE)
    print (soundProcess.pid)
    soundProcesses.append(soundProcess)
    soundProcessListLocations.append(fileLocation)
    soundProcessListWav.append(soundProcess.pid)
    return soundProcess.pid

def CreateSoundProcessMPG123(fileLocation, volume):
    print ("CreateSoundProcess ")
    print (fileLocation)
    global soundProcessList
    global soundProcessListLocations
    global soundProcesses
    volume = volume * 327
    soundProcess =  subprocess.Popen(["mpg123", fileLocation])
    print(soundProcess.pid)
    soundProcesses.append(soundProcess)
    soundProcessListLocations.append(fileLocation)
    soundProcessList.append(soundProcess.pid)
    return soundProcess.pid

def CreateSoundProcessMPG123ForWait(fileLocation, volume):
    print ("CreateSoundProcess ")
    print (fileLocation)
    global soundProcessList
    global soundProcessListLocations
    global soundProcesses
    volume = volume * 327
    soundProcess =  subprocess.Popen(["mpg123", "-f", "-" + str(volume), fileLocation])
    print(soundProcess.pid)
    soundProcesses.append(soundProcess)
    soundProcessListLocations.append(fileLocation)
    soundProcessList.append(soundProcess.pid)
    return soundProcess.pid

def CreateSoundProcessOMX(fileLocation, volume):
    print ("CreateSoundProcess ")
    print (fileLocation)
    global soundProcessList
    global soundProcessListLocations
    soundProcess =  subprocess.Popen(['/usr/bin/omxplayer', '-o', 'local', '--vol', volume, fileLocation], stdin=subprocess.PIPE)
    soundProcessListLocations.append(fileLocation)
    soundProcessList.append(soundProcess.pid)
    return soundProcess.pid

def IsSoundProcessActive():
    global soundProcessList
    global soundProcessListWav
    global soundProcesses
    returnValue = False
    for soundProcess in soundProcesses:
        if soundProcess.poll() is None:
            returnValue = True
            break
    for soundProcess in soundProcessList:
        if psutil.pid_exists(soundProcess):
            returnValue = True
            break
    if returnValue == False:
        for soundProcess in soundProcessListWav:
            if psutil.pid_exists(soundProcess):
                returnValue = True
                break
    
    return returnValue

def CleanUpSoundProcessList():
    global soundProcessList
    global soundProcessListWav
    for soundProcess in soundProcessList:
        KillSoundProcessByPID(soundProcess)
#        soundProcessList.remove(soundProcess)
    for soundProcess in soundProcessListWav:
        KillSoundProcessByPID(soundProcess)
#        soundProcessListWav.remove(soundProcess)

def KillSoundProcessByPID(pidToKill):
    print ("Kill PID") 
    print (pidToKill)
    global soundProcessListLocations
    locationIndex = 0
    os.system("kill " + str(pidToKill))
    print("killed " + str(pidToKill))
    for soundProcessLocation in soundProcessListLocations:
        if soundProcessLocation.find("/tmp/") >= 0:
            print ("Deleting " + soundProcessLocation)
            os.system('rm -f ' + soundProcessLocation)
            soundProcessListLocations.remove(soundProcessLocation)

def CreateVoiceOut(textToSpeak):
    fileName = '/tmp/test' + str(datetime.datetime.now()).split('.')[1] + '.wav'
    print (fileName)
    os.system('/usr/bin/pico2wave --lang=de-DE --wave=' + fileName + ' "' + textToSpeak + '"')
    return fileName


    
