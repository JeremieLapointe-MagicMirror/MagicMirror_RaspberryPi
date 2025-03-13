#!/usr/bin/env python3
from rpi_ws281x import PixelStrip, Color
import paho.mqtt.client as mqtt
import time
import json

# Configuration des LEDs WS2812B
LED_COUNT = 5        # Nombre de LEDs
LED_PIN = 18         # GPIO pin (18 utilise PWM)
LED_FREQ_HZ = 800000 # Fréquence du signal (800 KHz)
LED_DMA = 10         # Canal DMA
LED_BRIGHTNESS = 50  # Luminosité (0-255)
LED_INVERT = False   # Signal inversé
LED_CHANNEL = 0      # Canal PWM (0 ou 1)

# Initialisation de la bande LED
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Fonctions utilitaires pour les couleurs
def color(r, g, b):
    return Color(r, g, b)

# Couleurs prédéfinies
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
WHITE = color(255, 255, 255)
OFF = color(0, 0, 0)

# Configuration MQTT
MQTT_BROKER = "mirrormqtt.jeremielapointe.ca"
MQTT_PORT = 1883
MQTT_USER = "MirrorMQTT"
MQTT_PASSWORD = "Patate123"
MQTT_STATUS_TOPIC = "led/status"
MQTT_COMMAND_TOPIC = "led/command"

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au broker avec le code: {rc}")
    # S'abonner au topic de commande
    client.subscribe(MQTT_COMMAND_TOPIC)
    print(f"Abonné à {MQTT_COMMAND_TOPIC}")

def on_message(client, userdata, msg):
    print(f"Message reçu sur {msg.topic}: {msg.payload.decode()}")
    
    if msg.topic == MQTT_COMMAND_TOPIC:
        try:
            command = json.loads(msg.payload.decode())
            
            if "color" in command:
                color_name = command["color"]
                if color_name == "red":
                    set_led_color(client, RED)
                elif color_name == "green":
                    set_led_color(client, GREEN)
                elif color_name == "blue":
                    set_led_color(client, BLUE)
                elif color_name == "white":
                    set_led_color(client, WHITE)
                elif color_name == "off":
                    set_led_color(client, OFF)
                elif isinstance(color_name, dict) and "rgb" in color_name:
                    # Format attendu: {"color": {"rgb": [255, 0, 0]}}
                    rgb = color_name["rgb"]
                    c = color(rgb[0], rgb[1], rgb[2])
                    set_led_color(client, c)
            
            elif "state" in command:
                if command["state"] == "ON":
                    set_led_color(client, WHITE)
                else:
                    set_led_color(client, OFF)
                    
            elif "brightness" in command:
                # Valeur entre 0 et 255
                brightness = int(float(command["brightness"]) * 255)
                strip.setBrightness(brightness)
                strip.show()
                client.publish(MQTT_STATUS_TOPIC, json.dumps({"brightness": brightness/255}))
                
        except json.JSONDecodeError:
            print("Erreur: Le message n'est pas au format JSON valide")
        except Exception as e:
            print(f"Erreur lors du traitement du message: {str(e)}")

def set_led_color(client, color_value):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color_value)
    strip.show()
    
    # Détermine l'état pour le message de statut
    if color_value == OFF:
        status = "OFF"
    else:
        status = "ON"
    
    # Extrait les composantes RGB
    r = (color_value >> 16) & 0xFF
    g = (color_value >> 8) & 0xFF
    b = color_value & 0xFF
    
    # Publie le statut et la couleur
    status_message = json.dumps({
        "state": status,
        "color": {"r": r, "g": g, "b": b}
    })
    
    client.publish(MQTT_STATUS_TOPIC, status_message)
    print(f"LED {status} - Couleur: RGB({r}, {g}, {b})")

def test_leds():
    """Fonction pour tester toutes les LEDs au démarrage"""
    print("Test des LEDs...")
    
    # Test des couleurs de base
    for test_color in [RED, GREEN, BLUE, WHITE]:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, test_color)
        strip.show()
        time.sleep(0.5)
    
    # Test individuel de chaque LED
    for i in range(strip.numPixels()):
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, OFF)
        strip.setPixelColor(i, WHITE)
        strip.show()
        time.sleep(0.2)
    
    # Éteindre toutes les LEDs
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, OFF)
    strip.show()
    
    print("Test terminé")

def main():
    try:
        # Test initial des LEDs
        test_leds()
        
        # Création du client MQTT
        client = mqtt.Client()
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        
        # Attribution des callbacks
        client.on_connect = on_connect
        client.on_message = on_message
        
        # Connexion au broker
        print(f"Connexion au broker {MQTT_BROKER}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Démarrage de la boucle MQTT
        client.loop_start()
        
        # Éteindre les LEDs au démarrage
        set_led_color(client, OFF)
        
        # Boucle principale - garde le programme en vie
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme")
        # Éteindre les LEDs avant de quitter
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, OFF)
        strip.show()
        client.loop_stop()
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        # Tenter d'éteindre les LEDs en cas d'erreur
        try:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, OFF)
            strip.show()
        except:
            pass

if __name__ == "__main__":
    main()