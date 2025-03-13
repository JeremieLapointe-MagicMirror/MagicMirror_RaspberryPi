#!/usr/bin/env python3
from rpi_ws281x import PixelStrip, Color
import time

# Configuration minimale
LED_COUNT = 5          # Nombre de LEDs
LED_PIN = 18           # GPIO pin
LED_BRIGHTNESS = 255   # Luminosité maximale pour test
LED_STRIP_TYPE = 1     # SK6812 GRBW (0 pour RGBW)

# Version simplifiée de l'initialisation
strip = PixelStrip(LED_COUNT, LED_PIN, 800000, 10, False, LED_BRIGHTNESS, 0, LED_STRIP_TYPE)
strip.begin()

# Allumer toutes les LEDs en rouge vif
print("Allumage en rouge")
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(255, 0, 0))  # Rouge
strip.show()

# Maintenir allumé pendant 10 secondes
time.sleep(10)

# Éteindre toutes les LEDs
print("Extinction")
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()