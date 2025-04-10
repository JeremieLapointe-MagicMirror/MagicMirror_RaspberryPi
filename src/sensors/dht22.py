#!/usr/bin/env python3
import Adafruit_DHT
import time
from datetime import datetime

# Configuration
CAPTEUR = Adafruit_DHT.DHT22
PIN_DHT = 27 
DELAI = 5     # Lecture toutes les 5 secondes

print("Test du capteur DHT22...")
print("Appuyez sur Ctrl+C pour arrêter")
print("---------------------------------")

try:
    while True:
        # Lecture des données du capteur
        humidite, temperature = Adafruit_DHT.read_retry(CAPTEUR, PIN_DHT)
        
        # Horodatage
        horodatage = datetime.now().strftime("%H:%M:%S")
        
        # Affichage des données si lecture réussie
        if humidite is not None and temperature is not None:
            print(f"[{horodatage}] Température: {temperature:.1f}°C, Humidité: {humidite:.1f}%")
        else:
            print(f"[{horodatage}] Échec de lecture du capteur")
        
        # Attente avant prochaine lecture
        time.sleep(DELAI)
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")