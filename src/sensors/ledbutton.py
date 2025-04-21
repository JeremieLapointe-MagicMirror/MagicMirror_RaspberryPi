#!/usr/bin/env python3
# Code pour contrôler des LEDs NeoPixel avec un bouton tactile TTP223 en mode toggle
# Ce code est simplifié car le mode toggle est géré par le capteur lui-même

import time
import board
import neopixel
import RPi.GPIO as GPIO

# Configuration des broches
BUTTON_PIN = 17  # Broche GPIO pour le bouton TTP223 (à ajuster selon votre câblage)
PIXEL_PIN = board.D18  # Broche de données pour les NeoPixels
NUM_PIXELS = 5  # Limité à 5 LEDs pour la phase initiale

# Configuration des LED NeoPixel
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=0.5,
    auto_write=True,
    pixel_order=neopixel.GRB
)

# Couleur par défaut (blanc)
DEFAULT_COLOR = (255, 255, 255)

# Configuration du GPIO pour le bouton
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

def turn_on_leds():
    """Allume toutes les LEDs avec la couleur par défaut."""
    for i in range(NUM_PIXELS):
        pixels[i] = DEFAULT_COLOR
    pixels.show()
    
def turn_off_leds():
    """Éteint toutes les LEDs."""
    pixels.fill((0, 0, 0))
    pixels.show()

try:
    print("Programme démarré. Appuyez sur le bouton TTP223 pour allumer/éteindre les LEDs.")
    print("Assurez-vous que votre TTP223 est configuré en mode toggle (broche TOG connectée à VDD).")
    print("Appuyez sur Ctrl+C pour quitter.")
    
    # État initial des LEDs (éteintes)
    turn_off_leds()
    
    # En mode toggle, le capteur gère l'état lui-même
    last_state = GPIO.input(BUTTON_PIN)
    
    while True:
        # Lecture de l'état actuel du bouton
        current_state = GPIO.input(BUTTON_PIN)
        
        # Si l'état a changé, mettre à jour les LEDs
        if current_state != last_state:
            if current_state == GPIO.HIGH:
                print("LEDs allumées")
                turn_on_leds()
            else:
                print("LEDs éteintes")
                turn_off_leds()
            
            # Petit délai pour éviter des changements multiples trop rapides
            time.sleep(0.2)
            
        last_state = current_state
        
        # Court délai pour économiser le CPU
        time.sleep(0.05)
        
except KeyboardInterrupt:
    # Éteindre les LEDs avant de quitter
    turn_off_leds()
    GPIO.cleanup()
    print("\nProgramme arrêté proprement.")
except Exception as e:
    # En cas d'erreur, éteindre les LEDs et nettoyer le GPIO
    turn_off_leds()
    GPIO.cleanup()
    print(f"Une erreur s'est produite: {e}")