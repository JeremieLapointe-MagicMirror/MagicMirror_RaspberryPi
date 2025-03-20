#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Choisir un GPIO différent
PIN_PIR = 27  # Essayez un autre GPIO (27 = pin physique 13)

# Configuration GPIO en mode brut
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PIR, GPIO.IN)

print(f"Test PIR basique sur GPIO {PIN_PIR}")
print("Appuyez sur Ctrl+C pour quitter")

try:
    while True:
        # Lire directement l'état du GPIO
        etat = GPIO.input(PIN_PIR)
        print(f"État: {etat}")
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nTest terminé")