import time
import RPi.GPIO as GPIO

# Configuration de base
touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN)

try:
    print("Programme démarré. Touchez le capteur TTP223...")
    
    # État initial
    last_state = GPIO.input(touch_pin)
    print(f"État initial: {'HIGH' if last_state else 'LOW'}")
    
    while True:
        current_state = GPIO.input(touch_pin)
        
        # Afficher uniquement lors d'un changement d'état
        if current_state != last_state:
            print(f"[{time.ctime()}] État: {'HIGH' if current_state else 'LOW'}")
            last_state = current_state
            
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print("Programme interrompu!")
finally:
    GPIO.cleanup()