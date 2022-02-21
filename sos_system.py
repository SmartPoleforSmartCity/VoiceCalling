# Call pin
CALL_PIN = 22
# Number of seconds to keep the call active
DOORBELL_SCREEN_ACTIVE_S = 120
# ID of the JITSI meeting room
JITSI_ID = "SOS1" 
# Path to the SFX file
RING_SFX_PATH = None  # If None, no sound effect plays

import time
import os
import signal
import subprocess
import smtplib
import uuid

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO")


def show_screen():
    os.system("tvservice -p")
    os.system("xset dpms force on")


def hide_screen():
    os.system("tvservice -o")


def ring_doorbell(pin):
    GPIO.cleanup(pin)
    SoundEffect(RING_SFX_PATH).play()
    chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
    video_chat = VideoChat(chat_id)   
    show_screen()
    video_chat.start()

class SoundEffect:
    def __init__(self, filepath):
        self.filepath = filepath

    def play(self):
        if self.filepath:
            subprocess.Popen(["aplay", self.filepath])


class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return "https://meet.example.org/%s" % self.chat_id

    def start(self):
        if not self._process and self.chat_id:
            self._process = subprocess.Popen(["chromium-browser", "-kiosk", self.get_chat_url()])
        else:
            print("Already started or missing chat id")

    def end(self):
        if self._process:
            os.kill(self._process.pid, signal.SIGTERM)

class Doorbell:
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin

    def run(self):
        try:
            hide_screen()
            self._setup_gpio()
            self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")

    def _wait_forever(self):
        while True:
            time.sleep(0.1)

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)        
        
    def _cleanup(self):
        GPIO.cleanup(self._doorbell_button_pin)
        show_screen()

    def end_call(self): 
        self.end()
        self.hide_screen()

if __name__ == "__main__":
    doorbell = Doorbell(CALL_PIN)
    doorbell.run()
