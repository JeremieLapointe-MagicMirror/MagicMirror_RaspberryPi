#!/usr/bin/env python3
import time
import board
import adafruit_dht
from datetime import datetime

# Configuration - Remplacez board.D17 par le pin GPIO que vous utilisez
# D17 correspond au GPIO 17
PIN_DHT = board.D27
DELAI = 3  # Lecture toutes les 3 secondes

# Initialisation du capteur
dht = adafruit_dht.DHT22(PIN_DHT)

print("Test du capteur DHT22 avec CircuitPython...")
print("Appuyez sur Ctrl+C pour arrêter")
print("----------------------------------------")

try:
    while True:
        try:
            # Lecture des données du capteur
            temperature = dht.temperature
            humidite = dht.humidity
            
            # Horodatage
            horodatage = datetime.now().strftime("%H:%M:%S")
            
            # Affichage des données si lecture réussie
            print(f"[{horodatage}] Température: {temperature:.1f}°C, Humidité: {humidite:.1f}%")
            
        except RuntimeError as e:
            # Les erreurs de lecture sont courantes, on les affiche simplement
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur de lecture: {e}")
        
        # Attente avant prochaine lecture
        time.sleep(DELAI)
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")
finally:
    # Nettoyage
    dht.exit()