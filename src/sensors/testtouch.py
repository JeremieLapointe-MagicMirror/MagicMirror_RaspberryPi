import time
import RPi.GPIO as GPIO

# Configuration
touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN)  # Sans résistance de rappel pour commencer

try:
    print("Programme de diagnostic démarré. Appuyez sur Ctrl+C pour quitter.")
    print("Surveillez les changements d'état quand vous touchez le capteur.")
    
    previous_state = None
    while True:
        current_state = GPIO.input(touch_pin)
        
        # Afficher l'état uniquement s'il a changé
        if current_state != previous_state:
            print(f"[{time.ctime()}] État du capteur: {'HIGH (1)' if current_state else 'LOW (0)'}")
            previous_state = current_state
        
        time.sleep(0.05)  # Lecture plus rapide pour ne pas manquer de changements
        
except KeyboardInterrupt:
    print("Programme interrompu!")
    GPIO.cleanup()