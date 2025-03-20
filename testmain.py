#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Configuration
PIN_PIR = 4
DETECTION_ACTIVE = 0  # Signal BAS (0) pour détecter le mouvement

# Configuration GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PIR, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Activation pull-up

print("Test de détection PIR - Appuyez sur Ctrl+C pour quitter")
print("Initialisation...")
time.sleep(2)  # Court délai d'initialisation

try:
    while True:
        if GPIO.input(PIN_PIR) == DETECTION_ACTIVE:
            print("Présence humaine détectée!")
        else:
            print("Pas de présence détectée")
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")
    GPIO.cleanup()