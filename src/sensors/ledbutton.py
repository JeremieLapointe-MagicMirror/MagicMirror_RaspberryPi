#!/usr/bin/env python3
# Code pour contrôler des LEDs NeoPixel avec un bouton tactile TTP223
# Version finale et optimisée

import time
import board
import neopixel
import RPi.GPIO as GPIO

# Configuration des broches
BUTTON_PIN = 17  # Broche GPIO pour le bouton TTP223
PIXEL_PIN = board.D18  # Broche de données pour les NeoPixels
NUM_PIXELS = 5  # Nombre de LEDs NeoPixel

# Configuration des LED NeoPixel
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=0.5,  # Luminosité à 50%
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
    pixels.fill(DEFAULT_COLOR)
    
def turn_off_leds():
    """Éteint toutes les LEDs."""
    pixels.fill((0, 0, 0))

try:
    print("Programme démarré. Appuyez sur le bouton TTP223 pour allumer/éteindre les LEDs.")
    print("Appuyez sur Ctrl+C pour quitter.")
    
    # État initial des LEDs (éteintes)
    led_state = False
    turn_off_leds()
    
    while True:
        # Vérifier si le bouton est pressé (état haut)
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            # Basculer l'état des LEDs
            led_state = not led_state
            
            if led_state:
                turn_on_leds()
                print("LEDs allumées")
            else:
                turn_off_leds()
                print("LEDs éteintes")
                
            # Attendre que le bouton soit relâché
            while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                time.sleep(0.1)
                
            # Anti-rebond
            time.sleep(0.3)
            
        time.sleep(0.1)  # Délai de la boucle principale
        
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