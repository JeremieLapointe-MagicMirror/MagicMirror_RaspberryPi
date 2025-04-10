import time
import RPi.GPIO as GPIO

touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def touch_callback(channel):
    if not GPIO.input(channel):  # LOW = touché avec PUD_UP
        print(f"[{time.ctime()}] Capteur touché")

# Ajouter l'événement avec débouncing de 300ms
GPIO.add_event_detect(touch_pin, GPIO.FALLING, callback=touch_callback, bouncetime=300)

try:
    print("Programme démarré avec détection par événement.")
    print("Appuyez sur Ctrl+C pour quitter.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programme interrompu!")
    GPIO.cleanup()