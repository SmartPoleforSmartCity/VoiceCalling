import os
while True:
    state = int(input('input 1 --> bink\ninput 2 --> call\ninput : '))
    if state == 1 :
        command = "start cmd /k gpio.py"
        os.system(command)
    elif state == 2 :
        command = "start cmd /k client.py"
        os.system(command)