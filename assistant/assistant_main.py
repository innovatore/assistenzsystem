#!/usr/bin/python

import pigpio, time, os
import assistant_music
import assistant_newsfeed
import assistant_weather
import assistant_volumecontrol

pi = pigpio.pi()
if not pi.connected:
   exit()

pin1 = 16
pin2 = 24
pin3 = 12
pin4 = 18

glitchValue = 200
assistant_music.PlayWaitMusic()

os.system("amixer sset PCM,0 95%")

def InitializeData():
    assistant_music.musicPlayList = assistant_music.CreateMusicPlayList()
    assistant_newsfeed.newsList = assistant_newsfeed.LoadRSS("SPIEGEL")
    if assistant_newsfeed.newsList != 0:
        assistant_newsfeed.newsList.entries.append(assistant_newsfeed.LoadRSS("Bischof Bode").entries)
    if assistant_newsfeed.newsList != 0:
        assistant_newsfeed.newsList.entries.append(assistant_newsfeed.LoadRSS("STERN").entries)
    if assistant_newsfeed.newsList != 0:
        assistant_newsfeed.newsList.entries.append(assistant_newsfeed.LoadRSS("Boulevard").entries)
    assistant_weather.LoadWeatherData()

def InitializeButtons():
    pi.set_mode(pin1, pigpio.INPUT)
    pi.set_pull_up_down(pin1, pigpio.PUD_UP)  
    pi.set_mode(pin2, pigpio.INPUT)
    pi.set_pull_up_down(pin2, pigpio.PUD_UP)  
    pi.set_mode(pin3, pigpio.INPUT)
    pi.set_pull_up_down(pin3, pigpio.PUD_UP)  
    pi.set_mode(pin4, pigpio.INPUT)
    pi.set_pull_up_down(pin4, pigpio.PUD_UP)  
    
    cb1 = pi.callback(pin1, pigpio.FALLING_EDGE, assistant_newsfeed.PlayNews)
    pi.set_glitch_filter(pin1, glitchValue)
    cb1 = pi.callback(pin2, pigpio.FALLING_EDGE, assistant_music.PlaySong)
    pi.set_glitch_filter(pin2, glitchValue)
    cb1 = pi.callback(pin3, pigpio.FALLING_EDGE, assistant_weather.PlayTimeAndWeather)
    pi.set_glitch_filter(pin3, glitchValue)
    cb1 = pi.callback(pin4, pigpio.FALLING_EDGE, assistant_music.PlayError)
    pi.set_glitch_filter(pin4, glitchValue)

InitializeData()
InitializeButtons()
time.sleep(3)
assistant_music.SilenceSounds()
assistant_music.SaySomething("System gestartet, warte auf Eingabe.")

while True:
#    assistant_weather.LoadWeatherData()
    print(assistant_volumecontrol.Measure(pi))
