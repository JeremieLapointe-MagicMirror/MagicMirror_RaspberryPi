#!/usr/bin/env python3
import time
import json
from datetime import datetime
import signal
import sys

# Import des modules du projet
from src.config import MQTT_CONFIG, SENSOR_CONFIG
from src.sensors.temperature import get_cpu_temperature, format_temperature_message
from src.communication.mqtt_client import MQTTClient

# Variable globale pour le client MQTT
mqtt_client = None

# Handler pour arrêt propre
def signal_handler(sig, frame):
    print("\nArrêt du programme...")
    if mqtt_client:
        mqtt_client.disconnect()
    sys.exit(0)

# Configuration du gestionnaire de signal
signal.signal(signal.SIGINT, signal_handler)

def main():
    global mqtt_client
    
    # Initialisation du client MQTT
    mqtt_client = MQTTClient(
        MQTT_CONFIG['broker'],
        MQTT_CONFIG['port'],
        MQTT_CONFIG['username'],
        MQTT_CONFIG['password']
    )
    
    # Connexion au broker MQTT
    if not mqtt_client.connect():
        print("Impossible de se connecter au broker MQTT. Fin du programme.")
        return
    
    print("Programme de surveillance démarré")
    print("Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        last_temp_check = 0
        
        while True:
            current_time = time.time()
            
            # Publication périodique de la température
            if current_time - last_temp_check >= SENSOR_CONFIG['temperature_check_interval']:
                temperature = get_cpu_temperature()
                
                if temperature is not None:
                    # Préparation et publication du message de température
                    temp_message = format_temperature_message(temperature)
                    mqtt_client.publish(MQTT_CONFIG['topic_temperature'], temp_message)
                    
                    # Afficher pour debug
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Température CPU: {temperature:.2f}°C - Publiée sur MQTT")
                    
                    last_temp_check = current_time
            
            # Pause pour réduire l'utilisation CPU
            time.sleep(1)
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Nettoyage avant de quitter
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()