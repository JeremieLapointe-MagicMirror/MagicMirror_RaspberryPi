#!/usr/bin/env python3
from gpiozero import MotionSensor

# Utilisation du GPIO 17 au lieu du GPIO 4
pir = MotionSensor(17)

print("Test de capteur PIR avec gpiozero")
print("Initialisation du capteur...")
print("Capteur prêt!")

while True:
    print("Recherche de présence humaine...")
    pir.wait_for_motion()
    
    print("Présence humaine détectée!")
    pir.wait_for_no_motion()
    
    print("Plus de présence humaine détectée")