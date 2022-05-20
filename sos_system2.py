import time, os, signal, subprocess,smtplib, uuid
import requests
import cv2
import numpy as np
from datetime import datetime as date
import RPi.GPIO as GPIO

JITSI_ID = "test_sos1"
pid = None
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
en_button = False
start = False

def user_capture():
    name = file_name()
    cam = cv2.VideoCapture(0)
    ret,frame = cam.read()
    cv2.imwrite('/home/pi/Desktop/sos_capture/'+name, frame)
    cam.release()
    cv2.destroyAllWindows()
        
def file_name():
    time = date.now().strftime("%H%M%S_%d%m%Y")
    filename = "SOS1_{}.jpeg".format(time)
    return filename

def run():
    global start
    global en_button
    if not start:
        start = not start
        run_chat()
        info = {"status": 1}
        requests.post("http://34.143.237.67:8000/video_call", data=info)
        while True:
            result = requests.get("http://34.143.237.67:8000/video_call", data=info)
            result = result.json()
            if result == 0:
                print("stop")
                start = False
                break
        stop_chat()
        
            
def stop_chat():
    global pid
    os.kill(pid, signal.SIGTERM)
    time.sleep(0.5)
    _wait_forever()
    
def run_chat():
    global pid
    process = subprocess.Popen(["chromium-browser",'-kiosk', "https://meet.jit.si/%s"%JITSI_ID])
    pid = process.pid
    print(pid)
    
def _wait_forever():
    print("Starting SOS...")
    input = GPIO.input(22)
    while True:
        time.sleep(0.2)
        result = requests.get("http://34.143.237.67:8000/pole_button")
        result = result.json()
        if result == 0:
            en_button = False
        else:
            en_button = True
        if GPIO.input(22) == 0 and en_button == True:
            time.sleep(0.2)
            user_capture()
            time.sleep(1)
            run()
        
if __name__ == "__main__":
    _wait_forever()
