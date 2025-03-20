#!/usr/bin/env python3
from gpiozero import MotionSensor
import time
from datetime import datetime

# Configuration
PIN_PIR = 4
DELAI_REFRESH = 0.5  # Temps entre chaque rafraîchissement en secondes

# Initialisation du capteur
pir = MotionSensor(PIN_PIR)

print("Initialisation du capteur PIR...")
time.sleep(2)
print("Capteur prêt! En attente de mouvement...")

try:
    while True:
        # Attendre qu'un mouvement soit détecté
        pir.wait_for_motion()
        print("Mouvement détecté!")
        
        # Tant qu'il y a du mouvement, continuer à afficher le message
        while pir.motion_detected:
            horodatage = datetime.now().strftime("%H:%M:%S")
            print(f"[{horodatage}] Mouvement en cours...")
            time.sleep(DELAI_REFRESH)
        
        print("Plus de mouvement détecté.")
        print("En attente de nouveau mouvement...")

except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")