import os
import RPi.GPIO as GPIO
import threading
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)


def binkbtn():
    while True:
        state = GPIO.input(27)
        if state :
            GPIO.output(17,GPIO.LOW)
        else :
            GPIO.output(17,GPIO.HIGH)
        
def binkinput():
    while True:
        bink = int(input('input 0 --> off\ninput 1 --> on'))
        if bink == 1 :
            GPIO.output(10,GPIO.HIGH)
        elif bink == 0 :
            GPIO.output(10,GPIO.LOW)
        
def binktime():
    while True:
        h, m, s = datetime.now().strftime("%H:%M:%S").split(':')
        if h == 18 and m == 0 and  10 <= s <=30 :
            GPIO.output(9,GPIO.HIGH)
        else :
            GPIO.output(9,GPIO.LOW)
            
t1 = threading.Thread(target = binkbtn)
t2 = threading.Thread(target = binkinput)
t3 = threading.Thread(target = binktime)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

