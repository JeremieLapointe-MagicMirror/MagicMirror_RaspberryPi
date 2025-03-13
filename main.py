#!/usr/bin/env python3
from rpi_ws281x import PixelStrip, Color
import time

# Configuration des LEDs
LED_COUNT = 5        # Nombre de LEDs sur votre bande
LED_PIN = 18         # GPIO pin connectée aux pixels
LED_FREQ_HZ = 800000 # Fréquence du signal en hertz
LED_DMA = 10         # Canal DMA à utiliser
LED_BRIGHTNESS = 50  # Entre 0 (min) et 255 (max)
LED_INVERT = False   # Inverser le signal
LED_CHANNEL = 0      # Canal utilisé

# Création et initialisation de l'objet LED
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Définition de quelques couleurs
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
PURPLE = Color(128, 0, 128)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
OFF = Color(0, 0, 0)

def allumer_toutes(couleur, temps_attente=0.5):
    """Allume toutes les LEDs avec la couleur spécifiée"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, couleur)
    strip.show()
    time.sleep(temps_attente)

def animation_defilement(temps_attente=0.1):
    """Animation avec défilement de LED une par une"""
    # Éteindre toutes les LEDs
    allumer_toutes(OFF, 0)
    
    # Allumer une LED à la fois
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, RED)
        strip.show()
        time.sleep(temps_attente)
        strip.setPixelColor(i, OFF)
    
    # Allumer une LED à la fois en sens inverse
    for i in range(strip.numPixels()-1, -1, -1):
        strip.setPixelColor(i, BLUE)
        strip.show()
        time.sleep(temps_attente)
        strip.setPixelColor(i, OFF)

def animation_vague(temps_attente=0.1):
    """Animation en forme de vague avec plusieurs couleurs"""
    # Éteindre toutes les LEDs
    allumer_toutes(OFF, 0)
    
    # Animation de vague
    for i in range(strip.numPixels() + 3):
        # Éteindre toutes les LEDs
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, OFF)
        
        # Allumer les LEDs dans une séquence
        if i - 3 >= 0 and i - 3 < strip.numPixels():
            strip.setPixelColor(i - 3, BLUE)
        if i - 2 >= 0 and i - 2 < strip.numPixels():
            strip.setPixelColor(i - 2, CYAN)
        if i - 1 >= 0 and i - 1 < strip.numPixels():
            strip.setPixelColor(i - 1, GREEN)
        if i >= 0 and i < strip.numPixels():
            strip.setPixelColor(i, RED)
        
        strip.show()
        time.sleep(temps_attente)

# Programme principal
try:
    print('Programme de contrôle LED WS2812B')
    print('Appuyez sur Ctrl-C pour quitter')
    
    while True:
        # Test de différentes couleurs
        print('Test de couleurs simples')
        allumer_toutes(RED)
        allumer_toutes(GREEN)
        allumer_toutes(BLUE)
        allumer_toutes(WHITE)
        allumer_toutes(PURPLE)
        allumer_toutes(YELLOW)
        allumer_toutes(CYAN)
        
        # Animation de défilement
        print('Animation de défilement')
        animation_defilement()
        
        # Animation de vague
        print('Animation de vague')
        animation_vague()
        
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à la sortie
    allumer_toutes(OFF, 0)
    print('Programme arrêté')