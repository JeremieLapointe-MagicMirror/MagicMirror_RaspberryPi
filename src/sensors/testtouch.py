import time
import RPi.GPIO as GPIO

# Configuration
touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Résistance de rappel activée

# Variables pour le débouncing
last_state = GPIO.input(touch_pin)
last_change_time = time.time()
debounce_delay = 0.1  # 100ms de délai

try:
    print("Programme démarré avec débouncing. Appuyez sur Ctrl+C pour quitter.")
    
    while True:
        current_state = GPIO.input(touch_pin)
        current_time = time.time()
        
        # Vérifier si l'état a changé et si suffisamment de temps s'est écoulé
        if current_state != last_state and (current_time - last_change_time) > debounce_delay:
            if current_state == 0:  # LOW = touché avec PUD_UP
                print(f"[{time.ctime()}] Capteur touché")
            else:
                print(f"[{time.ctime()}] Capteur relâché")
            
            last_state = current_state
            last_change_time = current_time
            
        time.sleep(0.01)  # Petite pause pour ne pas surcharger le CPU
        
except KeyboardInterrupt:
    print("Programme interrompu!")
    GPIO.cleanup()