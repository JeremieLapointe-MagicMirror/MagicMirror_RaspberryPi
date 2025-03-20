#!/usr/bin/env python3
from gpiozero import MotionSensor
import time
from datetime import datetime

# Configuration
PIN_PIR = 4
DELAI_VERIFICATION = 0.2  # Temps entre chaque vérification
DELAI_DETECTION = 3  # Temps en secondes pour considérer qu'il n'y a plus de mouvement

# Initialisation du capteur
pir = MotionSensor(PIN_PIR)

print("Initialisation du capteur PIR...")
time.sleep(2)
print("Capteur prêt! En attente de mouvement...")

try:
    mouvement_actif = False
    dernier_mouvement = 0
    
    while True:
        maintenant = time.time()
        
        # Si mouvement détecté
        if pir.motion_detected:
            dernier_mouvement = maintenant
            
            # Si c'est un nouveau mouvement
            if not mouvement_actif:
                mouvement_actif = True
                print("Mouvement détecté!")
            
            # Si mouvement en cours, rafraîchir l'affichage
            horodatage = datetime.now().strftime("%H:%M:%S")
            print(f"[{horodatage}] Mouvement en cours...")
        
        # Si pas de mouvement détecté mais état actif
        elif mouvement_actif and (maintenant - dernier_mouvement) > DELAI_DETECTION:
            mouvement_actif = False
            print("Plus de mouvement détecté.")
            print("En attente de nouveau mouvement...")
            
        time.sleep(DELAI_VERIFICATION)
            
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")