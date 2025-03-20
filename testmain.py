#!/usr/bin/env python3
from gpiozero import MotionSensor
import time
import sys

# Configuration
PIN_PIR = 7
TEMPS_STABILISATION = 60  # secondes

# Initialisation avec paramètres de sensibilité ajustés
# Diminuer threshold rend le capteur moins sensible
# Augmenter queue_len exige plus de détections consécutives
pir = MotionSensor(PIN_PIR, threshold=0.7, queue_len=5)

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
        
        # Attendre un mouvement
        pir.wait_for_motion()
        print("Présence humaine détectée!")
        
        # Attendre la fin du mouvement
        pir.wait_for_no_motion()
        print("Plus de présence humaine détectée")
        
        # Petit délai pour éviter les rebonds
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")