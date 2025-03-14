#!/usr/bin/env python3
import time
from rpi_ws281x import PixelStrip, Color

# Configuration de la bande LED
LED_COUNT = 5          # Nombre de LEDs
LED_PIN = 18           # GPIO pin (18 utilise PWM matériel)
LED_FREQ_HZ = 800000   # Fréquence du signal (800 kHz)
LED_DMA = 10           # Canal DMA
LED_BRIGHTNESS = 100   # Luminosité (0-255)
LED_INVERT = False     # Inverser le signal
LED_CHANNEL = 0        # 0 pour les GPIO 10, 12, 18, 21
LED_STRIP_TYPE = 0     # Type de LED: WS2812 = 1 (RGB), WS2811 = 0 (GRB)

# Initialisation de la bande LED
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP_TYPE)
strip.begin()

# Fonction pour créer des couleurs
def color(red, green, blue):
    """Convertit les valeurs RGB en une valeur de couleur unique"""
    # L'ordre dépend du type de LED, ajustez si nécessaire
    return Color(red, green, blue)

# Couleurs prédéfinies
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
YELLOW = color(255, 255, 0)
PURPLE = color(255, 0, 255)
CYAN = color(0, 255, 255)
WHITE = color(255, 255, 255)
OFF = color(0, 0, 0)

def clear():
    """Éteint toutes les LEDs"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, OFF)
    strip.show()

def test_colors():
    """Test simple de toutes les couleurs prédéfinies"""
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, WHITE]
    
    print("Test des couleurs de base...")
    for color in colors:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(1)
    
    clear()
    print("Test des couleurs terminé")

def test_individual_leds():
    """Teste chaque LED individuellement"""
    print("Test de chaque LED individuellement...")
    
    for i in range(strip.numPixels()):
        clear()
        print(f"Allumage de la LED {i+1}")
        strip.setPixelColor(i, WHITE)
        strip.show()
        time.sleep(1)
    
    clear()
    print("Test des LEDs individuelles terminé")

def test_chase():
    """Effet de poursuite simple"""
    print("Test d'animation (chase)...")
    
    for test_color in [RED, BLUE, GREEN]:
        for i in range(strip.numPixels() * 3):  # Faire plusieurs tours
            clear()
            strip.setPixelColor(i % strip.numPixels(), test_color)
            strip.show()
            time.sleep(0.1)
    
    clear()
    print("Test d'animation terminé")

def test_brightness():
    """Teste différents niveaux de luminosité"""
    print("Test de luminosité...")
    
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, WHITE)
    
    for brightness in [25, 75, 125, 175, 255]:
        print(f"Luminosité: {brightness}/255")
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(1)
    
    # Remettre à la luminosité par défaut
    strip.setBrightness(LED_BRIGHTNESS)
    clear()
    print("Test de luminosité terminé")

def rainbow_cycle(wait_ms=20, iterations=1):
    """Affiche un cycle arc-en-ciel sur toutes les LEDs"""
    print("Test arc-en-ciel...")
    
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            # Calculer la couleur pour chaque pixel
            wheel_pos = (i * 256 // strip.numPixels() + j) & 255
            
            # Fonction pour obtenir la couleur arc-en-ciel
            if wheel_pos < 85:
                strip.setPixelColor(i, Color(wheel_pos * 3, 255 - wheel_pos * 3, 0))
            elif wheel_pos < 170:
                wheel_pos -= 85
                strip.setPixelColor(i, Color(255 - wheel_pos * 3, 0, wheel_pos * 3))
            else:
                wheel_pos -= 170
                strip.setPixelColor(i, Color(0, wheel_pos * 3, 255 - wheel_pos * 3))
        
        strip.show()
        time.sleep(wait_ms / 1000.0)
    
    clear()
    print("Test arc-en-ciel terminé")

def main_menu():
    """Menu principal pour sélectionner les tests"""
    while True:
        print("\n----- MENU DE TEST BANDE LED -----")
        print("1. Test de toutes les couleurs")
        print("2. Test de chaque LED individuelle")
        print("3. Test d'animation (chase)")
        print("4. Test de luminosité")
        print("5. Test arc-en-ciel")
        print("6. Allumer en blanc")
        print("7. Éteindre toutes les LEDs")
        print("0. Quitter")
        
        choice = input("Choisissez une option (0-7): ")
        
        if choice == '1':
            test_colors()
        elif choice == '2':
            test_individual_leds()
        elif choice == '3':
            test_chase()
        elif choice == '4':
            test_brightness()
        elif choice == '5':
            rainbow_cycle()
        elif choice == '6':
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, WHITE)
            strip.show()
            print("LEDs allumées en blanc")
        elif choice == '7':
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
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, BLUE)
            strip.show()
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