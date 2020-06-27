Assistant-System for blind People

Plays Audio-Files, narrates the time, the local weather and the content of rss-newsfeeds at the push of a button.

Work in Progress.

Components:
A Box, a Speaker, a RaspberryPi v3, 4 Buttons, a Powerswitch, a Mobile-Internet-Dongle, a Powerbank, 
a few Cables, an USB-Car-Loading-Adapter, a Potentiometer, a Condensator,
Your favorite Soundfiles and a Python Script.

How to start:
Check out the sources and run assistant_main.py

Script Language: 
Python 3

Dependencies:
PigPio, MPG123, pico2wave, psutil, feedparser, api.ipstack.com, api.openweathermap.org

How it works
With crontab, two @Reboot-directives are implemented: starting of first pigpiod and then assistant_main.py
On boot of the raspberry, the assistant_main.py: 

- Registers Callback Functions for the buttons attached to the GPIO-Pins: 12, 16, 18 and 24.
- Those are attached to the Buttons - a List of Soundfiles is generated from the contents of a folder.
- Multiple RSS-Feeds are parsed for news.
- Location is retrieved from ipstack api and
  weatherdata is retrieved from openweathermap.
- The Time and date is read from the Raspberry's System Time.
- An endless loop is started to keep the program running and the Assistant-System is ready for Input.
- Callback Functions are executed asynchronously on button push.
