import time
import pigpio
import array
import os

#pi = pigpio.pi()
#if not pi.connected:
#   exit()

pin = 17

def Measure(pi):
    iteration = 0
    iterationCount = 10
    values = array.array('i')
    while iteration < iterationCount:
        counter = 0
        pi.set_mode(pin, pigpio.OUTPUT)

        pi.write(pin, 0)
        time.sleep(0.01)

        pi.set_mode(pin, pigpio.INPUT)
        value = pi.read(pin)
        while value == 0:
            counter = counter + 1
            value = pi.read(pin)
        values.append(counter)
        iteration = iteration + 1
    result = 0
    for item in values:
        result = result + item
    newVolume = result / iterationCount
    setVolume = 0
    if newVolume == 0:
        setVolume = 0
    elif newVolume > 0 and newVolume < 25:
        setVolume = 80
    elif newVolume > 25 and newVolume < 50:
        setVolume = 85
    elif newVolume > 50 and newVolume < 75:
        setVolume = 90
    elif newVolume > 75 and newVolume < 100:
        setVolume = 95
    elif newVolume > 100 and newVolume < 200:
        setVolume = 100
    os.system("amixer sset PCM,0 " + str(setVolume) + "%")
    return result / iterationCount

#while True:
#    print (Measure())
