import time
import RPi.GPIO as GPIO

# Configuration du capteur tactile TP223
touch_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin, GPIO.IN) 

# Fonction de détection du toucher
def touch_det(pin):
    return GPIO.input(pin)  # Retourne 1 quand touché, 0 sinon

print("Test du capteur tactile TP223 - Appuyez sur CTRL+C pour quitter")
print("En attente de touches...")

etat_precedent = False

try:
    while True:
        etat_actuel = touch_det(touch_pin)
        
        # Détection du changement d'état (front montant)
        if etat_actuel and not etat_precedent:
            print('['+time.ctime()+'] - Touch Detected')
        
        etat_precedent = etat_actuel
        time.sleep(0.1)  # Délai réduit pour une meilleure réactivité

except KeyboardInterrupt:
    print('Programme interrompu!')
    GPIO.cleanup()