#!/usr/bin/env python3
from rpi_ws281x import PixelStrip, Color
import time

# Configuration simple
strip = PixelStrip(5, 18, 800000, 10, False, 255, 0)
strip.begin()

# Allumer toutes les LEDs en blanc
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(255, 255, 255))
strip.show()

# Attendre 10 secondes
time.sleep(10)

# Éteindre
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()