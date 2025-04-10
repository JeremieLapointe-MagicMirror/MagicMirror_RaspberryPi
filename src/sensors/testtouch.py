import time
import RPi.GPIO as GPIO
import sys

# Configuration
touch_pin = 17

# Réinitialiser proprement le GPIO avant de commencer
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables pour le "software debouncing"
last_touch_time = 0
touch_cooldown = 0.5  # 500ms entre détections

try:
    print("Programme démarré avec debouncing logiciel. Appuyez sur Ctrl+C pour quitter.")
    
    while True:
        # Lecture de l'état actuel
        current_state = GPIO.input(touch_pin)
        current_time = time.time()
        
        # Détection d'une pression (LOW avec PUD_UP)
        if current_state == 0 and (current_time - last_touch_time) > touch_cooldown:
            print(f"[{time.ctime()}] Capteur touché")
            last_touch_time = current_time
            
        time.sleep(0.05)  # Courte pause
        
except KeyboardInterrupt:
    print("Programme interrompu!")
except Exception as e:
    print(f"Erreur: {e}")
finally:
    GPIO.cleanup()
    sys.exit(0)