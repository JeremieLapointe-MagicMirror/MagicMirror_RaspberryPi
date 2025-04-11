#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime
import ssl

# Configuration GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)

# Configuration MQTT
MQTT_BROKER = "mirrormqtt.jeremielapointe.ca"
MQTT_PORT = 8883
MQTT_USER = "MirrorMQTT"
MQTT_PASSWORD = "Patate123"
MQTT_TOPIC = "serial/etatpir"

# Initialiser le client MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Configuration SSL pour MQTTS
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
client.tls_set_context(context)

# Se connecter au broker
def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        print(f"Connecté au broker MQTT: {MQTT_BROKER}")
        return True
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return False

# Publier l'état du PIR
def publish_pir_state(motion_detected):
    message = {
        "motion_detected": motion_detected,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device": "raspberry_pi_4"
    }
    
    try:
        result = client.publish(MQTT_TOPIC, json.dumps(message))
        if result.rc == 0:
            status = "Ouvert" if motion_detected else "Fermé"
            print(f"État publié: {status}")
        else:
            print(f"Échec de publication: {result.rc}")
    except Exception as e:
        print(f"Erreur de publication: {e}")

# Programme principal
print("Démarrage de la surveillance de mouvement PIR...")
time.sleep(2)  # Délai pour stabilisation du capteur
print("Prêt! Appuyez sur Ctrl+C pour quitter.")

try:
    # Connexion MQTT
    if not connect_mqtt():
        exit(1)
    
    # Variables pour éviter les publications redondantes
    last_state = None
    
    while True:
        current_state = GPIO.input(PIR_PIN)
        
        # Publier seulement si l'état a changé
        if current_state != last_state:
            publish_pir_state(current_state == 1)
            last_state = current_state
        
        # Afficher l'état actuel
        if current_state:
            print('Motion Detected')
        
        time.sleep(0.5)  # Délai pour éviter une surcharge
        
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur")
finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
    print("Nettoyage terminé.")