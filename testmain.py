#!/usr/bin/env python3
from gpiozero import MotionSensor
import time
import sys

# Configuration
PIN_PIR = 4
TEMPS_STABILISATION = 10  # réduit pour faciliter les tests

# Initialisation avec logique inversée
# when_activated et when_deactivated sont inversés ici
pir = MotionSensor(PIN_PIR, threshold=0.5, queue_len=1, pull_up=True, active_state=False)

# Période de stabilisation
print(f"Initialisation du capteur PIR, veuillez patienter {TEMPS_STABILISATION} secondes...")
for i in range(TEMPS_STABILISATION, 0, -1):
    sys.stdout.write(f"\rStabilisation: {i} secondes restantes...")
    sys.stdout.flush()
    time.sleep(1)
print("\nCapteur PIR prêt!")

# Boucle principale
try:
    while True:
        print("Recherche de présence humaine...")
        
        # Attendre un mouvement (avec logique inversée)
        pir.wait_for_motion()
        print("Présence humaine détectée!")
        
        # Attendre la fin du mouvement (avec logique inversée)
        pir.wait_for_no_motion()
        print("Plus de présence humaine détectée")
        
        # Petit délai
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")