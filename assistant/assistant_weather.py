# -*- coding: UTF-8 -*-
import urllib.request, subprocess, json, datetime, locale
import assistant_soundprocess
from time import *
from random import seed
from random import choice

cancelWeather = False
gong = '/home/pi/Desktop/Atone.wav'
beep = '/home/pi/Desktop/beep.mp3'
seed()
weatherString = list()

def PlayTimeAndWeather(g, l, t):
    global cancelWeather
    if assistant_soundprocess.IsSoundProcessActive() == False:
        cancelWeather = False
        
    if cancelWeather == True:
        cancelWeather = False
        assistant_soundprocess.CreateSoundProcessMPG123(beep, 100)
        sleep(0.5)
        assistant_soundprocess.CleanUpSoundProcessList()
    else:
        cancelWeather = True
        assistant_soundprocess.CleanUpSoundProcessList()
        PlaySystemTime()
        
def PlaySystemTime():
    assistant_soundprocess.CreateSoundProcessAplay(gong, 100)
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    outputstr = "Es ist " + datetime.datetime.now().strftime("%H:%M")
    outputstr = outputstr + " " + choice(weatherString)
    assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), 100)
        
        
def PlayWeather(weatherString = weatherString):
    
    return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(choice(weatherString)), 100)
    
def LoadWeatherData(weatherString = weatherString):
    error = False
    try:
        print ("PlayWeather start")
        
        locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
        proc = subprocess.Popen(["curl ifconfig.me"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print ("program output:", out)
        ipAdress = out.decode("utf-8")
        print (ipAdress)
        urlIpLocation = "http://api.ipstack.com/" + ipAdress + "?access_key=[Your Api Access Token]"
        ipLocationRaw = urllib.request.urlopen(urlIpLocation).read()
        print (ipLocationRaw)
        try:
            ipLocationRaw.decode("utf-8").index("latitude")
            js = json.loads(ipLocationRaw.decode("utf-8"))
            print (ipLocationRaw)
            longitude = str(js["longitude"])
            latitude = str(js["latitude"])
            print (longitude + " at " + latitude)
            urlWeather = "http://api.openweathermap.org/data/2.5/weather?lat=" + latitude + "&lon=" + longitude + "&lang=de&units=metric&appid=[Your Api Access Token]"
            weatherDataRaw = urllib.request.urlopen(urlWeather).read()
            print (weatherDataRaw)
            weatherData = json.loads(weatherDataRaw.decode("utf-8"))
            print (weatherData)
            try:
                outputstr = ", Wetter in {} ".format(js["region_name"])
            except KeyError:
                outputstr = ""
            try:  
                outputstr = outputstr + "{}, ".format(weatherData["name"])
            except KeyError:
                outputstr = outputstr
            try:       
                outputstr = outputstr + "{}".format(str(weatherData["weather"]).split(": ")[3].split(",")[0])
            except KeyError:
                outputstr = outputstr
            print(format(weatherData["main"]["temp"],'n') + " Hallo " + locale.format("%.2f",12000,1))
            try:
                weatherString.append(outputstr + ", bei {} Grad Celsius.".format(format(weatherData["main"]["temp"], 'n')))
            except KeyError:
                outputstr = outputstr
        except ValueError:
            outputstr = "Kein Netzwerk"
            weatherString.append(outputstr)
            error = True
        print (outputstr)
        print ("PlayWeather end")
        if error == True:
            outputstr = "Kein Netzwerk zum Laden der Wetterdaten."
        else:
            outputstr = "Wetterdaten erfolgreich geladen."
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), 100)
    except IOError:
        outputstr = "Kein Netzwerk. Die Systemzeit ist " + str(datetime.datetime.now())
        weatherString.append(outputstr)
        assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), 100)
        print ("PlayWeather end")
        return assistant_soundprocess.CreateSoundProcessAplay(assistant_soundprocess.CreateVoiceOut(outputstr), 100)

