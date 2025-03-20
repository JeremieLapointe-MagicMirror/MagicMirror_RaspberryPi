#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime
import signal
import sys
from gpiozero import MotionSensor

# Configuration
PIN_PIR = 4               # GPIO pin pour le capteur PIR
TEMPS_STABILISATION = 60  # Temps pour que le capteur se stabilise (secondes)
TEMPS_ENTRE_LOGS = 1      # Intervalle pour l'enregistrement des états (secondes)
FICHIER_LOG = "pir_log.txt"  # Fichier pour sauvegarder les détections

class TesteurPIR:
    def __init__(self, pin=PIN_PIR):
        self.pir = MotionSensor(pin)
        self.pir.threshold = 0.5  # Valeur par défaut, ajustable
        self.debut_detection = None
        self.fin_detection = None
        self.total_detections = 0
        self.en_cours_detection = False
        self.temps_debut = time.time()
        
        # Configuration de gestionnaire pour l'arrêt propre
        signal.signal(signal.SIGINT, self.arreter_proprement)
        
        # Ouvrir fichier log
        self.fichier = open(FICHIER_LOG, "a")
        self.enregistrer_log("=== DÉBUT DU TEST PIR ===")
        self.enregistrer_log(f"Date/heure: {datetime.datetime.now()}")
        self.enregistrer_log(f"Pin GPIO: {pin}")
        self.enregistrer_log(f"Seuil de détection: {self.pir.threshold}")
        
    def enregistrer_log(self, message):
        """Enregistre un message dans le fichier log et l'affiche"""
        horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        message_log = f"{horodatage} - {message}"
        print(message_log)
        self.fichier.write(message_log + "\n")
        self.fichier.flush()
        
    def demarrer_stabilisation(self):
        """Permet au capteur PIR de se stabiliser"""
        self.enregistrer_log(f"Stabilisation du capteur pendant {TEMPS_STABILISATION} secondes...")
        for i in range(TEMPS_STABILISATION, 0, -1):
            sys.stdout.write(f"\rStabilisation: {i} secondes restantes...")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r" + " " * 50 + "\r")
        self.enregistrer_log("Capteur stabilisé. Début du test.")
        
    def surveiller_mouvement(self):
        """Fonction principale de surveillance des mouvements"""
        try:
            while True:
                # Vérifier l'état actuel du capteur
                if self.pir.motion_detected and not self.en_cours_detection:
                    self.debut_detection = time.time()
                    self.en_cours_detection = True
                    self.total_detections += 1
                    self.enregistrer_log(f"DÉTECTION #{self.total_detections}: Mouvement détecté!")
                
                elif not self.pir.motion_detected and self.en_cours_detection:
                    self.fin_detection = time.time()
                    duree = round(self.fin_detection - self.debut_detection, 2)
                    self.en_cours_detection = False
                    self.enregistrer_log(f"Fin de détection - Durée: {duree} secondes")
                
                # Affichage périodique de l'état du capteur (valeur brute)
                valeur_brute = self.pir.value
                self.enregistrer_log(f"État brut du capteur: {valeur_brute}")
                
                time.sleep(TEMPS_ENTRE_LOGS)
                
        except KeyboardInterrupt:
            self.arreter_proprement(None, None)
            
    def arreter_proprement(self, signum, frame):
        """Arrête proprement le programme et enregistre les statistiques"""
        duree_totale = round(time.time() - self.temps_debut, 2)
        
        self.enregistrer_log("\n=== RÉSULTATS DU TEST ===")
        self.enregistrer_log(f"Durée totale du test: {duree_totale} secondes")
        self.enregistrer_log(f"Nombre total de détections: {self.total_detections}")
        if duree_totale > 0:
            detections_par_minute = round((self.total_detections * 60) / duree_totale, 2)
            self.enregistrer_log(f"Taux de détection: {detections_par_minute} détections/minute")
        
        self.enregistrer_log("=== FIN DU TEST PIR ===\n")
        self.fichier.close()
        sys.exit(0)

# Fonction principale
def main():
    testeur = TesteurPIR(PIN_PIR)
    testeur.demarrer_stabilisation()
    testeur.surveiller_mouvement()

if __name__ == "__main__":
    main()