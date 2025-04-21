#!/usr/bin/env python3
# Code pour contrôler des LEDs NeoPixel avec un bouton tactile TTP223
# Ce code utilise RPi.GPIO pour le bouton et rpi_ws281x pour les NeoPixels

import time
import board
import neopixel
import RPi.GPIO as GPIO

# Configuration des broches
BUTTON_PIN = 17  # Broche GPIO pour le bouton TTP223 (à ajuster selon votre câblage)
PIXEL_PIN = board.D18  # Broche de données pour les NeoPixels (D18 est GPIO 18)
NUM_PIXELS = 5  # Limitation à 5 LEDs pour la phase initiale

# Configuration des LED NeoPixel
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=0.5,  # 50% de luminosité
    auto_write=True,
    pixel_order=neopixel.GRB  # La plupart des NeoPixels utilisent l'ordre GRB
)

# Couleur par défaut (blanc)
DEFAULT_COLOR = (255, 255, 255)

# Configuration du GPIO pour le bouton
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

# Variables d'état
led_state = False  # État initial: éteint
last_button_state = GPIO.input(BUTTON_PIN)
last_time_pressed = 0
DEBOUNCE_TIME = 0.2  # Temps de rebond en secondes

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
    print("Appuyez sur Ctrl+C pour quitter.")
    
    while True:
        # Lecture de l'état actuel du bouton
        current_button_state = GPIO.input(BUTTON_PIN)
        
        # Gestion de l'anti-rebond et détection de front montant (appui)
        current_time = time.time()
        if (current_button_state != last_button_state and 
            current_button_state == GPIO.HIGH and 
            current_time - last_time_pressed > DEBOUNCE_TIME):
            
            # Inverser l'état des LEDs
            led_state = not led_state
            
            if led_state:
                print("LEDs allumées")
                turn_on_leds()
            else:
                print("LEDs éteintes")
                turn_off_leds()
            
            last_time_pressed = current_time
            
        # Enregistrer l'état du bouton pour la prochaine itération
        last_button_state = current_button_state
        
        # Court délai pour économiser le CPU
        time.sleep(0.01)
        
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