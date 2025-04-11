import time
import json
from datetime import datetime
import signal
import sys
import RPi.GPIO as GPIO
from src.config import MQTT_CONFIG, SENSOR_CONFIG
from src.sensors.temperature import get_cpu_temperature, format_temperature_message
from src.communication.mqtt_client import MQTTClient

# Variable globale pour le client MQTT
mqtt_client = None

# Configuration GPIO pour le PIR
PIR_PIN = SENSOR_CONFIG['motion_pin']  # Utilise la valeur de config.py
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIR_PIN, GPIO.IN)

# Handler pour arrêt propre
def signal_handler(sig, frame):
    print("\nArrêt du programme...")
    if mqtt_client:
        mqtt_client.disconnect()
    GPIO.cleanup()
    sys.exit(0)

# Configuration du gestionnaire de signal
signal.signal(signal.SIGINT, signal_handler)

# Fonction pour publier l'état du capteur PIR
def publish_pir_state(motion_detected):
    if mqtt_client:
        message = {
            "motion_detected": motion_detected,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device": "raspberry_pi_4"
        }
        
        mqtt_client.publish(MQTT_CONFIG['topic_pir_state'], json.dumps(message))
        
        # Afficher pour debug
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Ouvert" if motion_detected else "Fermé"
        print(f"[{timestamp}] État écran: {status} - Publié sur MQTT")

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
        last_pir_state = None
        
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
            
            # Vérification de l'état du capteur PIR
            current_pir_state = GPIO.input(PIR_PIN)
            
            # Publier l'état seulement s'il a changé
            if current_pir_state != last_pir_state:
                publish_pir_state(current_pir_state == 1)
                last_pir_state = current_pir_state
            
            # Pause pour réduire l'utilisation CPU
            time.sleep(0.5)
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Nettoyage avant de quitter
        mqtt_client.disconnect()
        GPIO.cleanup()

if __name__ == "__main__":
    main()