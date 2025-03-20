#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from gpiozero import MotionSensor
from datetime import datetime

# Configuration
PIN_PIR = 4  # GPIO pin pour le capteur PIR

# Initialisation du capteur
pir = MotionSensor(PIN_PIR)

print("Test de capteur PIR - Appuyez sur Ctrl+C pour quitter")
print("Attente de 2 secondes pour initialisation du capteur...")
time.sleep(2)  # Court délai d'initialisation
print("Capteur prêt!")

# État précédent pour détecter les changements
etat_precedent = False

try:
    while True:
        # Obtenir l'état actuel
        etat_actuel = pir.motion_detected
        
        # Afficher uniquement lors d'un changement d'état
        if etat_actuel != etat_precedent:
            timestamp = datetime.now().strftime("%H:%M:%S")
            if etat_actuel:
                print(f"[{timestamp}] ✓ MOUVEMENT DÉTECTÉ")
            else:
                print(f"[{timestamp}] ✗ PAS DE MOUVEMENT")
            
            etat_precedent = etat_actuel
        
        # Attente très courte pour réactivité
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\nTest terminé.")