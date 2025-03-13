#!/usr/bin/env python3
from rpi_ws281x import PixelStrip, Color
import time

# Configuration des LEDs
LED_COUNT = 5        # Nombre de LEDs
LED_PIN = 18         # GPIO pin
LED_FREQ_HZ = 800000 # Fréquence 
LED_DMA = 10         # Canal DMA
LED_BRIGHTNESS = 50  # Luminosité (0-255)
LED_INVERT = False   # Signal inversé
LED_CHANNEL = 0      # Canal PWM 

# Initialisation
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Couleurs
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
OFF = Color(0, 0, 0)

def allumer_toutes(couleur):
    """Allume toutes les LEDs avec la couleur spécifiée"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, couleur)
    strip.show()
    
def test_couleurs():
    """Teste différentes couleurs"""
    print("Rouge")
    allumer_toutes(RED)
    time.sleep(1)
    
    print("Vert")
    allumer_toutes(GREEN)
    time.sleep(1)
    
    print("Bleu")
    allumer_toutes(BLUE)
    time.sleep(1)
    
    print("Blanc")
    allumer_toutes(WHITE)
    time.sleep(1)
    
    print("Éteint")
    allumer_toutes(OFF)
    time.sleep(1)

def test_individuel():
    """Allume chaque LED une par une"""
    print("Test individuel des LEDs")
    for i in range(strip.numPixels()):
        # Éteindre toutes les LEDs
        allumer_toutes(OFF)
        
        # Allumer une seule LED
        strip.setPixelColor(i, RED)
        strip.show()
        print(f"LED {i}")
        time.sleep(0.5)

# Programme principal
try:
    print("Programme de test LED WS2812B")
    print("Appuyez sur Ctrl+C pour quitter")
    
    while True:
        test_couleurs()
        test_individuel()
        
except KeyboardInterrupt:
    print("\nProgramme arrêté")
    allumer_toutes(OFF)  # Éteindre les LEDs en quittant