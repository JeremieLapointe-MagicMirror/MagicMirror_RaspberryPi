#!/usr/bin/env python3
from gpiozero import MotionSensor
import time
from datetime import datetime

# Configuration
PIN_PIR = 4
DELAI_VERIFICATION = 0.5  # Augmenté pour réduire la charge CPU

print("Initialisation du capteur PIR sur GPIO", PIN_PIR)
print("Vérifiez votre câblage :")
print("- VCC du capteur → 5V du Raspberry Pi")
print("- GND du capteur → Ground du Raspberry Pi")
print("- OUT du capteur → GPIO", PIN_PIR)
print("\nInitialisation du capteur...")

# Initialisation du capteur avec paramètres explicites
pir = MotionSensor(PIN_PIR, queue_len=1, sample_rate=10, threshold=0.5)

time.sleep(2)  # Attente pour stabilisation
print("Capteur prêt! État initial:", "Mouvement détecté" if pir.motion_detected else "Pas de mouvement")
print("En attente... Appuyez sur Ctrl+C pour quitter")

try:
    activations = 0
    while True:
        if pir.motion_detected:
            activations += 1
            horodatage = datetime.now().strftime("%H:%M:%S")
            print(f"[{horodatage}] Mouvement détecté! (Total: {activations})")
        
        # Toujours indiquer l'état actuel
        current_state = "ACTIF" if pir.motion_detected else "INACTIF"
        print(f"\rÉtat du capteur: {current_state}", end="")
        
        time.sleep(DELAI_VERIFICATION)
            
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")