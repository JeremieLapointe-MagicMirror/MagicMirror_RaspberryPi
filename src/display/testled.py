import board
import neopixel
import time

# Configuration des LEDs NeoPixel
# GPIO 15 correspond à board.D15 dans CircuitPython
pixel_pin = board.D18
num_pixels = 5
ORDER = neopixel.GRB  # L'ordre des couleurs peut être différent selon votre modèle de LED

# Initialisation des pixels
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Couleurs
RED = (255, 0, 0)
OFF = (0, 0, 0)

def clear():
    """Éteindre toutes les LEDs"""
    pixels.fill(OFF)
    pixels.show()

# Allumer les LEDs une par une
def sequence():
    clear()
    time.sleep(1)
    
    # Allumer chaque LED l'une après l'autre
    for i in range(num_pixels):
        clear()  # Éteindre toutes les LEDs
        pixels[i] = RED  # Allumer la LED actuelle
        pixels.show()
        time.sleep(0.5)  # Pause de 0.5 seconde
    
    # Éteindre toutes les LEDs à la fin
    clear()

# Boucle principale
try:
    while True:
        sequence()
        time.sleep(1)  # Pause entre chaque séquence

except KeyboardInterrupt:
    clear()  # Éteindre les LEDs en quittant
    print("Programme arrêté")
