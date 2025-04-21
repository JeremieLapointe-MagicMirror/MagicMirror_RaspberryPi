#!/usr/bin/env python3
# Code de test pour le capteur TTP223
import RPi.GPIO as GPIO
import time

# Configuration de la broche
BUTTON_PIN = 17  # Ajustez selon votre branchement

# Configuration du GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

try:
    print("Test du capteur TTP223. Appuyez sur Ctrl+C pour quitter.")
    print("Touchez le capteur et observez les changements d'état.")
    
    last_state = GPIO.input(BUTTON_PIN)
    print(f"État initial du capteur: {'Touché' if last_state else 'Non touché'}")
    
    while True:
        # Lecture de l'état actuel
        current_state = GPIO.input(BUTTON_PIN)
        
        # Affichage de l'état seulement s'il a changé
        if current_state != last_state:
            print(f"État du capteur: {'Touché' if current_state else 'Non touché'}")
            last_state = current_state
        
        # Court délai
        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nTest terminé.")