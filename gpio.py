import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
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
        bink = int(input('input 1 --> on \ninput 0 --> off\ninput : '))
        if bink :
            GPIO.output(10,GPIO.HIGH)
        else:
            GPIO.output(10,GPIO.LOW)
            
t1 = threading.Thread(target = binkbtn)
t2 = threading.Thread(target = binkinput)

t1.start()
t2.start()

t1.join()
t2.join()