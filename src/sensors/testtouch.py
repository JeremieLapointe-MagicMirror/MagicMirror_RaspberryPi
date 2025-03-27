import time
import RPi.GPIO as GPIO

# Configuration du capteur tactile TP223
touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Fonction de détection du toucher
def touch_det(pin):
    touch = GPIO.input(pin)
    return touch

print("Test du capteur tactile TP223 - Appuyez sur CTRL+C pour quitter")
print("En attente de touches...")

try:
    while True:
        if touch_det(touch_pin): 
            print('['+time.ctime()+'] - Touch Detected')
        time.sleep(0.2)

except KeyboardInterrupt:
    print('Programme interrompu!')
    GPIO.cleanup()