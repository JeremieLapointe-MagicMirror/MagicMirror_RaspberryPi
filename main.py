#!/usr/bin/env python3

# Pour installer les bibliothèques requises:
# sudo pip3 install --break-system-packages adafruit-circuitpython-neopixel

import board
import neopixel
import time

# Configuration
pixel_pin = board.D18  # Pin GPIO 18
num_pixels = 5        # Nombre de LEDs
brightness = 0.2      # Luminosité (0.0 à 1.0)

# Initialisation de la bande LED
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False
)

# Couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

def test_couleurs():
    """Test des différentes couleurs"""
    print("Rouge")
    pixels.fill(RED)
    pixels.show()
    time.sleep(1)
    
    print("Vert")
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    
    print("Bleu")
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)
    
    print("Blanc")
    pixels.fill(WHITE)
    pixels.show()
    time.sleep(1)
    
    print("Éteint")
    pixels.fill(OFF)
    pixels.show()
    time.sleep(1)

def test_individuel():
    """Test de chaque LED individuellement"""
    print("Test individuel des LEDs")
    for i in range(num_pixels):
        pixels.fill(OFF)  # Éteindre toutes les LEDs
        pixels[i] = RED   # Allumer une seule LED
        pixels.show()
        print(f"LED {i}")
        time.sleep(0.5)

try:
    print("Programme de test LED avec neopixel")
    print("Appuyez sur Ctrl+C pour quitter")
    
    while True:
        test_couleurs()
        test_individuel()
        
except KeyboardInterrupt:
    print("\nProgramme arrêté")
    pixels.fill(OFF)  # Éteindre les LEDs en quittant
    pixels.show()