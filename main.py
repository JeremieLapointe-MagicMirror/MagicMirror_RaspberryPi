#!/usr/bin/env python3
import time
import board
import neopixel
import paho.mqtt.client as mqtt
import json

# Configuration pour l'anneau NeoPixel
pixel_pin = board.D18  # GPIO 18
num_pixels = 35        # Nombre de LEDs sur l'anneau
brightness = 0.3       # Luminosité (0.0 à 1.0)
ORDER = neopixel.GRB   # L'ordre des couleurs peut être GRB ou RGB

# Initialisation de l'anneau LED
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)

# Configuration MQTT
MQTT_BROKER = "mirrormqtt.jeremielapointe.ca"
MQTT_PORT = 1883
MQTT_USER = "MirrorMQTT"
MQTT_PASSWORD = "Patate123"
MQTT_STATUS_TOPIC = "led/statusaa"
MQTT_COMMAND_TOPIC = "led/command"

# Définition des couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# Mode LED actuel
current_mode = "off"
current_color = OFF

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au broker avec le code: {rc}")
    # S'abonner au topic de commande après connexion
    client.subscribe(MQTT_COMMAND_TOPIC)
    print(f"Abonné à {MQTT_COMMAND_TOPIC}")
    # Publier un message de statut initial
    update_status(client)

def on_message(client, userdata, msg):
    global current_mode, current_color
    
    print(f"Message reçu sur {msg.topic}: {msg.payload.decode()}")
    
    try:
        command = json.loads(msg.payload.decode())
        
        if "color" in command:
            color_name = command["color"]
            if color_name == "red":
                set_color(RED)
                current_color = RED
            elif color_name == "green":
                set_color(GREEN)
                current_color = GREEN
            elif color_name == "blue":
                set_color(BLUE)
                current_color = BLUE
            elif color_name == "yellow":
                set_color(YELLOW)
                current_color = YELLOW
            elif color_name == "purple":
                set_color(PURPLE)
                current_color = PURPLE
            elif color_name == "cyan":
                set_color(CYAN)
                current_color = CYAN
            elif color_name == "white":
                set_color(WHITE)
                current_color = WHITE
            elif color_name == "off":
                set_color(OFF)
                current_color = OFF
            elif isinstance(color_name, dict) and "rgb" in color_name:
                # Format attendu: {"color": {"rgb": [255, 0, 0]}}
                rgb = color_name["rgb"]
                custom_color = (rgb[0], rgb[1], rgb[2])
                set_color(custom_color)
                current_color = custom_color
        
        elif "mode" in command:
            mode = command["mode"]
            current_mode = mode
            
            if mode == "solid":
                set_color(current_color)
            elif mode == "rainbow":
                # Démarrer animation arc-en-ciel dans un thread séparé
                print("Mode arc-en-ciel activé")
                # La boucle principale gèrera l'animation
            elif mode == "spinner":
                # Démarrer animation spinner dans un thread séparé
                print("Mode spinner activé")
                # La boucle principale gèrera l'animation
            elif mode == "chase":
                # Démarrer animation chase dans un thread séparé
                print("Mode chase activé")
                # La boucle principale gèrera l'animation
            elif mode == "off":
                set_color(OFF)
                current_color = OFF
        
        elif "brightness" in command:
            # Valeur entre 0.0 et 1.0
            brightness = float(command["brightness"])
            pixels.brightness = min(max(brightness, 0.0), 1.0)
            pixels.show()
        
        elif "state" in command:
            if command["state"] == "ON":
                if current_color == OFF:
                    current_color = WHITE
                set_color(current_color)
                current_mode = "solid"
            else:
                set_color(OFF)
                current_mode = "off"
                current_color = OFF
        
        # Mettre à jour le statut après chaque changement
        update_status(client)
            
    except json.JSONDecodeError:
        print("Erreur: Le message n'est pas au format JSON valide")
    except Exception as e:
        print(f"Erreur lors du traitement du message: {str(e)}")

def update_status(client):
    """Envoie l'état actuel au broker MQTT"""
    
    # Déterminer l'état à partir de la couleur actuelle
    state = "OFF" if current_color == OFF else "ON"
    
    # Convertir la couleur en RGB pour le message
    if isinstance(current_color, tuple) and len(current_color) >= 3:
        color_info = {"r": current_color[0], "g": current_color[1], "b": current_color[2]}
    else:
        color_info = {"r": 0, "g": 0, "b": 0}
    
    # Créer le message de statut
    status_message = json.dumps({
        "state": state,
        "mode": current_mode,
        "brightness": pixels.brightness,
        "color": color_info
    })
    
    # Publier le statut
    client.publish(MQTT_STATUS_TOPIC, status_message)
    print(f"Statut publié: {status_message}")

def set_color(color):
    """Définit une couleur uniforme pour tout l'anneau"""
    pixels.fill(color)
    pixels.show()

def color_chase(color, wait=0.01):
    """Animation de poursuite d'une couleur autour de l'anneau"""
    for i in range(num_pixels):
        pixels[i] = color
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

def rainbow_cycle(wait=0.01):
    """Animation arc-en-ciel circulant autour de l'anneau"""
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def spinner(color=WHITE, background=OFF, wait=0.05, length=5):
    """Effet de rotation autour de l'anneau"""
    for i in range(num_pixels):
        pixels.fill(background)
        
        # Allumer un segment de LEDs qui se déplace
        for j in range(length):
            pixel_index = (i + j) % num_pixels
            pixels[pixel_index] = color
            
        pixels.show()
        time.sleep(wait)

def run_animation():
    """Exécute l'animation actuellement sélectionnée"""
    global current_mode, current_color
    
    if current_mode == "rainbow":
        rainbow_cycle(0.01)
    elif current_mode == "spinner":
        spinner(color=current_color if current_color != OFF else WHITE)
    elif current_mode == "chase":
        # Sauvegarde la couleur actuelle
        old_color = current_color if current_color != OFF else WHITE
        # Éteint toutes les LEDs
        pixels.fill(OFF)
        pixels.show()
        # Animation de poursuite
        color_chase(old_color)
        # Remet toutes les LEDs à la couleur
        pixels.fill(old_color)
        pixels.show()

def main():
    # Création du client MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    # Attribution des callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connexion au broker
        print(f"Connexion au broker {MQTT_BROKER}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Démarrage de la boucle MQTT
        client.loop_start()
        
        # Éteindre les LEDs au démarrage
        set_color(OFF)
        current_mode = "off"
        
        # Animation initiale de démarrage
        print("Animation de démarrage...")
        spinner(color=BLUE, wait=0.02, length=5)
        set_color(OFF)
        
        # Publier l'état initial
        update_status(client)
        
        # Boucle principale
        while True:
            # Exécuter l'animation si un mode d'animation est actif
            if current_mode in ["rainbow", "spinner", "chase"]:
                run_animation()
            else:
                # Pause pour réduire l'utilisation CPU
                time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme")
        # Éteindre les LEDs avant de quitter
        set_color(OFF)
        client.loop_stop()
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        # Éteindre les LEDs en cas d'erreur
        set_color(OFF)

if __name__ == "__main__":
    main()