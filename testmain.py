#!/usr/bin/env python3
import time
import board
import neopixel

# Configuration pour la bande LED
PIXEL_PIN = board.D18    # GPIO 18 (PIN physique 12)
NUM_PIXELS = 5           # Nombre de LEDs sur la bande
BRIGHTNESS = 0.3         # Luminosité initiale (0.0 à 1.0)
ORDER = neopixel.GRB     # L'ordre des couleurs (GRB est courant pour de nombreuses LED NeoPixel)

# Initialisation des LEDs
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=BRIGHTNESS, 
    auto_write=False,    # Nécessite pixels.show() pour afficher les changements
    pixel_order=ORDER
)

# Couleurs prédéfinies
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

def clear():
    """Éteint toutes les LEDs"""
    pixels.fill(OFF)
    pixels.show()

def test_colors():
    """Test simple de toutes les couleurs prédéfinies"""
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, WHITE]
    
    print("Test des couleurs de base...")
    for color in colors:
        pixels.fill(color)
        pixels.show()
        time.sleep(1)
    
    clear()
    print("Test des couleurs terminé")

def test_individual_leds():
    """Teste chaque LED individuellement"""
    print("Test de chaque LED individuellement...")
    
    for i in range(NUM_PIXELS):
        clear()
        print(f"Allumage de la LED {i+1}")
        pixels[i] = WHITE
        pixels.show()
        time.sleep(1)
    
    clear()
    print("Test des LEDs individuelles terminé")

def test_chase():
    """Effet de poursuite simple"""
    print("Test d'animation (chase)...")
    
    for color in [RED, BLUE, GREEN]:
        for i in range(NUM_PIXELS * 3):  # Faire plusieurs tours
            clear()
            pixels[i % NUM_PIXELS] = color
            pixels.show()
            time.sleep(0.1)
    
    clear()
    print("Test d'animation terminé")

def test_brightness():
    """Teste différents niveaux de luminosité"""
    print("Test de luminosité...")
    
    pixels.fill(WHITE)
    
    for brightness in [0.1, 0.3, 0.5, 0.8, 1.0]:
        print(f"Luminosité: {brightness}")
        pixels.brightness = brightness
        pixels.show()
        time.sleep(1)
    
    clear()
    print("Test de luminosité terminé")

def main_menu():
    """Menu principal pour sélectionner les tests"""
    while True:
        print("\n----- MENU DE TEST BANDE LED -----")
        print("1. Test de toutes les couleurs")
        print("2. Test de chaque LED individuelle")
        print("3. Test d'animation (chase)")
        print("4. Test de luminosité")
        print("5. Allumer en blanc")
        print("6. Éteindre toutes les LEDs")
        print("0. Quitter")
        
        choice = input("Choisissez une option (0-6): ")
        
        if choice == '1':
            test_colors()
        elif choice == '2':
            test_individual_leds()
        elif choice == '3':
            test_chase()
        elif choice == '4':
            test_brightness()
        elif choice == '5':
            pixels.fill(WHITE)
            pixels.show()
            print("LEDs allumées en blanc")
        elif choice == '6':
            clear()
            print("LEDs éteintes")
        elif choice == '0':
            clear()
            print("Fin du programme")
            break
        else:
            print("Option invalide, veuillez réessayer")

if __name__ == "__main__":
    try:
        print("Initialisation de la bande LED...")
        clear()  # S'assurer que toutes les LEDs sont éteintes au démarrage
        
        # Animation de démarrage simple
        for i in range(NUM_PIXELS):
            pixels[i] = BLUE
            pixels.show()
            time.sleep(0.1)
        time.sleep(0.5)
        clear()
        
        print("Bande LED initialisée avec succès!")
        main_menu()
        
    except KeyboardInterrupt:
        print("\nProgramme arrêté par l'utilisateur")
        clear()  # Éteindre les LEDs avant de quitter
    except Exception as e:
        print(f"Erreur: {str(e)}")
        clear()  # Éteindre les LEDs en cas d'erreur