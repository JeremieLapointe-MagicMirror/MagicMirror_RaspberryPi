#!/usr/bin/env python3
# Version de debug pour contrôler des LEDs NeoPixel avec un capteur TTP223
import time
import board
import neopixel
import RPi.GPIO as GPIO

# Configuration des broches
BUTTON_PIN = 17  # Ajustez selon votre branchement
PIXEL_PIN = board.D18  # Ajustez selon votre branchement
NUM_PIXELS = 5

# Configuration des LEDs NeoPixel
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=0.5,
    auto_write=True,
    pixel_order=neopixel.GRB
)

# Configuration du GPIO pour le bouton
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

def turn_on_leds():
    print("Allumage des LEDs...")
    pixels.fill((255, 255, 255))  # Blanc
    
def turn_off_leds():
    print("Extinction des LEDs...")
    pixels.fill((0, 0, 0))

try:
    print("Programme démarré avec debugging.")
    print(f"Broche du bouton: GPIO{BUTTON_PIN}, Broche des LEDs: GPIO18")
    print("Appuyez sur Ctrl+C pour quitter.")
    
    # État initial
    led_state = False
    turn_off_leds()  # Éteindre au démarrage
    
    # Afficher l'état initial du bouton
    initial_button_state = GPIO.input(BUTTON_PIN)
    print(f"État initial du bouton: {initial_button_state} ({'Haut' if initial_button_state else 'Bas'})")
    
    while True:
        # Lecture et affichage de l'état du bouton
        current_state = GPIO.input(BUTTON_PIN)
        print(f"État du bouton: {current_state} ({'Haut' if current_state else 'Bas'})")
        
        # Vérifier si le bouton est pressé (état haut)
        if current_state == GPIO.HIGH:
            print("Bouton détecté à l'état HAUT")
            
            # Basculer l'état des LEDs
            led_state = not led_state
            
            if led_state:
                turn_on_leds()
            else:
                turn_off_leds()
                
            # Attendre que le bouton soit relâché
            print("Attente du relâchement du bouton...")
            while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                time.sleep(0.1)
            print("Bouton relâché")
            
            # Anti-rebond supplémentaire
            time.sleep(0.5)
            
        time.sleep(0.2)  # Délai de la boucle principale
        
except KeyboardInterrupt:
    turn_off_leds()
    GPIO.cleanup()
    print("\nProgramme arrêté.")
except Exception as e:
    print(f"Erreur: {e}")
    turn_off_leds()
    GPIO.cleanup()