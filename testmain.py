#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Configuration
PIN_PIR = 4

# Configuration du GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PIR, GPIO.IN)

print("Test de diagnostic PIR - Appuyez sur Ctrl+C pour quitter")
print("État initial du capteur...")

# Déterminer automatiquement l'état actif/inactif
time.sleep(3)  # Attendre un moment pour une lecture stable
etat_initial = GPIO.input(PIN_PIR)
print(f"État initial détecté : {'HAUT (1)' if etat_initial else 'BAS (0)'}")

# Détermine quelle valeur représente une détection
print("Pour déterminer quel état représente une détection:")
print("1. Assurez-vous qu'il n'y a PAS de mouvement devant le capteur")
print("2. Puis, après quelques secondes, bougez devant le capteur")
print("3. Observez les changements d'état")

try:
    dernier_etat = None
    while True:
        etat_actuel = GPIO.input(PIN_PIR)
        
        # N'afficher que lorsque l'état change
        if etat_actuel != dernier_etat:
            horodatage = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{horodatage}] État du capteur : {'HAUT (1)' if etat_actuel else 'BAS (0)'}")
            dernier_etat = etat_actuel
        
        time.sleep(0.1)  # Vérification rapide sans surcharger le CPU
        
except KeyboardInterrupt:
    print("\nTest terminé")
    GPIO.cleanup()