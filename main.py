#!/usr/bin/env python3
import time
import board
import neopixel

# Configuration pour l'anneau NeoPixel
pixel_pin = board.D18  # GPIO 18
num_pixels = 35        # Nombre de LEDs sur l'anneau
brightness = 0.2       # Luminosité (0.0 à 1.0)
ORDER = neopixel.GRB   # L'ordre des couleurs peut être GRB ou RGB

# Initialisation de l'anneau LED
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)

# Définition des couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

def fill_color(color, wait=0.05):
    """Remplit tout l'anneau d'une seule couleur"""
    pixels.fill(color)
    pixels.show()
    time.sleep(wait)

def color_chase(color, wait=0.01):
    """Animation de poursuite d'une couleur autour de l'anneau"""
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    time.sleep(0.5)

def rainbow_cycle(wait=0.01):
    """Animation arc-en-ciel circulant autour de l'anneau"""
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    """Génère un spectre de couleurs semblable à un arc-en-ciel"""
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

def spinner(color=WHITE, background=OFF, wait=0.05, length=5):
    """Effet de rotation autour de l'anneau"""
    for i in range(num_pixels * 3):  # Faire trois tours complets
        pixels.fill(background)
        
        # Allumer un segment de LEDs qui se déplace
        for j in range(length):
            pixel_index = (i + j) % num_pixels
            pixels[pixel_index] = color
            
        pixels.show()
        time.sleep(wait)

try:
    print("Test de l'anneau NeoPixel à 35 LEDs")
    print("Appuyez sur Ctrl+C pour quitter")
    
    while True:
        # Test 1: Couleurs unies
        print("Test des couleurs unies")
        for color in [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, WHITE]:
            fill_color(color, 0.5)
        fill_color(OFF, 0.5)
        
        # Test 2: Poursuite de couleur
        print("Test de poursuite de couleur")
        color_chase(RED)
        color_chase(GREEN)
        color_chase(BLUE)
        fill_color(OFF, 0.5)
        
        # Test 3: Arc-en-ciel
        print("Animation arc-en-ciel")
        rainbow_cycle(0.01)
        fill_color(OFF, 0.5)
        
        # Test 4: Spinner
        print("Animation spinner")
        spinner(color=BLUE, wait=0.03, length=5)
        fill_color(OFF, 0.5)
        
except KeyboardInterrupt:
    # Éteindre toutes les LEDs en sortant
    fill_color(OFF, 0)
    print("\nProgramme arrêté")