#!/usr/bin/env python3
from gpiozero import MotionSensor
import time
from datetime import datetime

# Configuration
PIN_PIR = 4
DELAI_INIT = 3  # Secondes d'initialisation

# Initialisation du capteur
pir = MotionSensor(PIN_PIR)

print("Initialisation du capteur PIR...")
time.sleep(DELAI_INIT)
print("Capteur prêt! En attente de mouvement...")

try:
    while True:
        # Attendre qu'un mouvement soit détecté
        pir.wait_for_motion()
        horodatage = datetime.now().strftime("%H:%M:%S")
        print(f"[{horodatage}] Mouvement détecté!")
        
        # Attendre la fin du mouvement
        pir.wait_for_no_motion()
        horodatage = datetime.now().strftime("%H:%M:%S")
        print(f"[{horodatage}] Mouvement terminé")
        print("En attente de nouveau mouvement...")

except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")