import time
import RPi.GPIO as GPIO

touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def touch_det(pin):
    return GPIO.input(pin)

try:
    while True:
        state = touch_det(touch_pin)
        print(f'[{time.ctime()}] - État du bouton: {state}')
        time.sleep(0.2)
except KeyboardInterrupt:
    print('interrupted!')
    GPIO.cleanup()