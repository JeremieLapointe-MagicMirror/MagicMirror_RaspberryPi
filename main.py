#!/usr/bin/env python3
import board
import neopixel
import paho.mqtt.client as mqtt
import time
import json

# Configuration des LEDs WS2812B
LED_PIN = board.D18  # GPIO 18
NUM_PIXELS = 5       # Nombre de LEDs sur votre bande
ORDER = neopixel.GRB # L'ordre des couleurs peut être GRB ou RGB

# Initialisation de la bande LED
pixels = neopixel.NeoPixel(
    LED_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Couleurs prédéfinies
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# Configuration MQTT
MQTT_BROKER = "mirrormqtt.jeremielapointe.ca"
MQTT_PORT = 1883
MQTT_USER = "MirrorMQTT"
MQTT_PASSWORD = "Patate123"
MQTT_STATUS_TOPIC = "led/status"
MQTT_COMMAND_TOPIC = "led/command"  # Pour recevoir des commandes

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
                color = command["color"]
                if color == "red":
                    set_led_color(client, RED)
                elif color == "green":
                    set_led_color(client, GREEN)
                elif color == "blue":
                    set_led_color(client, BLUE)
                elif color == "white":
                    set_led_color(client, WHITE)
                elif color == "off":
                    set_led_color(client, OFF)
                elif "rgb" in color:
                    # Format attendu: {"color": {"rgb": [255, 0, 0]}}
                    rgb_values = tuple(color["rgb"])
                    set_led_color(client, rgb_values)
            
            elif "state" in command:
                if command["state"] == "ON":
                    set_led_color(client, WHITE)
                else:
                    set_led_color(client, OFF)
                    
            elif "brightness" in command:
                # Valeur entre 0.0 et 1.0
                brightness = float(command["brightness"])
                pixels.brightness = min(max(brightness, 0.0), 1.0)
                pixels.show()
                client.publish(MQTT_STATUS_TOPIC, json.dumps({"brightness": brightness}))
                
        except json.JSONDecodeError:
            print("Erreur: Le message n'est pas au format JSON valide")
        except Exception as e:
            print(f"Erreur lors du traitement du message: {str(e)}")

def set_led_color(client, color):
    pixels.fill(color)
    pixels.show()
    
    # Détermine l'état pour le message de statut
    if color == OFF:
        status = "OFF"
    else:
        status = "ON"
    
    # Publie le statut et la couleur
    status_message = json.dumps({
        "state": status,
        "color": {"r": color[0], "g": color[1], "b": color[2]}
    })
    
    client.publish(MQTT_STATUS_TOPIC, status_message)
    print(f"LED {status} - Couleur: RGB{color}")

def test_leds():
    """Fonction pour tester toutes les LEDs au démarrage"""
    print("Test des LEDs...")
    
    # Test des couleurs de base
    for color in [RED, GREEN, BLUE, WHITE]:
        pixels.fill(color)
        pixels.show()
        time.sleep(0.5)
    
    # Test individuel de chaque LED
    pixels.fill(OFF)
    pixels.show()
    for i in range(NUM_PIXELS):
        pixels[i] = WHITE
        pixels.show()
        time.sleep(0.2)
        pixels[i] = OFF
        pixels.show()
    
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
        pixels.fill(OFF)
        pixels.show()
        client.loop_stop()
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        # Éteindre les LEDs en cas d'erreur
        if 'pixels' in locals():
            pixels.fill(OFF)
            pixels.show()

if __name__ == "__main__":
    main()