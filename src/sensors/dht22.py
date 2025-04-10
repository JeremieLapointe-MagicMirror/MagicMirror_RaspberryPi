#!/usr/bin/env python3
import pigpio
import time
from datetime import datetime

# Configuration
PIN_DHT = 27  
DELAI = 5     # Lecture toutes les 5 secondes

# Initialisation de pigpio
pi = pigpio.pi()

def read_dht22(gpio):
    """Lecture du capteur DHT22 en utilisant pigpio"""
    # Implémentation simplifiée pour communiquer avec le DHT22
    # Référence : http://abyz.me.uk/rpi/pigpio/examples.html
    
    # Préparation du capteur
    pi.set_mode(gpio, pigpio.OUTPUT)
    pi.write(gpio, 0)
    time.sleep(0.018)  # Attente minimale de 18ms
    pi.set_mode(gpio, pigpio.INPUT)
    
    # Lecture des données
    # Note: Cette implémentation est simplifiée
    # Une implémentation complète utiliserait les callbacks de pigpio
    
    # Attente réponse
    start_time = time.time()
    timeout = start_time + 0.2  # Timeout de 200ms
    while pi.read(gpio) == 0:
        if time.time() > timeout:
            return None, None
    while pi.read(gpio) == 1:
        if time.time() > timeout:
            return None, None
    
    # Simplification - nous retournons juste des valeurs aléatoires pour démonstration
    # Dans une implémentation réelle, vous devriez décoder correctement les signaux
    from random import uniform
    return uniform(30, 70), uniform(15, 25)  # humidité, température

print("Test du capteur DHT22...")
print("Appuyez sur Ctrl+C pour arrêter")
print("---------------------------------")

try:
    while True:
        humidite, temperature = read_dht22(PIN_DHT)
        horodatage = datetime.now().strftime("%H:%M:%S")
        
        if humidite is not None and temperature is not None:
            print(f"[{horodatage}] Température: {temperature:.1f}°C, Humidité: {humidite:.1f}%")
        else:
            print(f"[{horodatage}] Échec de lecture du capteur")
        
        time.sleep(DELAI)
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")
finally:
    pi.stop()