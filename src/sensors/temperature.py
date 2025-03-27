import time
from datetime import datetime
import json
import ssl
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration MQTT depuis les variables d'environnement
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtts://mirrormqtt.jeremielapointe.ca")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "MirrorMQTT")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "Patate123")
MQTT_TOPIC = os.getenv("MQTT_TOPIC_TEMPERATURE", "mm/temperature")

# Supprimer le préfixe "mqtts://" s'il existe
if MQTT_BROKER.startswith("mqtts://"):
    MQTT_BROKER = MQTT_BROKER[8:]

def get_cpu_temperature():
    """Récupère la température CPU du Raspberry Pi en degrés Celsius"""
    try:
        # Ouvrir le fichier contenant la température
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0  # Convertir en degrés Celsius
        return temp
    except Exception as e:
        print(f"Erreur lors de la lecture de la température: {e}")
        return None

def format_temperature_message(temperature):
    """Crée un message formaté avec la température"""
    return {
        "temperature": round(temperature, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device": "raspberry_pi_4"
    }

def setup_mqtt_client():
    """Configure et retourne un client MQTT"""
    # Initialisation du client
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # Configuration SSL/TLS
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    client.tls_set_context(context)
    
    # Callback de connexion
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connecté au broker MQTT {MQTT_BROKER}")
        else:
            print(f"Échec de la connexion MQTT avec le code: {rc}")
    
    client.on_connect = on_connect
    
    return client

def main():
    # Configuration du client MQTT
    mqtt_client = setup_mqtt_client()
    
    try:
        # Connexion au broker MQTT
        print(f"Connexion au broker MQTT {MQTT_BROKER}:{MQTT_PORT}...")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        
        print("Surveillance de la température du Raspberry Pi")
        print("Appuyez sur Ctrl+C pour arrêter le programme")
        print("-" * 50)
        
        # Boucle principale
        while True:
            # Obtenir la température
            temperature = get_cpu_temperature()
            
            if temperature is not None:
                # Afficher la température avec l'horodatage
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Température CPU: {temperature:.2f}°C")
                
                # Formater et publier le message MQTT
                temp_message = format_temperature_message(temperature)
                result = mqtt_client.publish(MQTT_TOPIC, json.dumps(temp_message))
                
                if result.rc == 0:
                    print(f"✓ Message publié sur {MQTT_TOPIC}")
                else:
                    print(f"✕ Échec de publication: {result.rc}")
            
            # Attendre avant la prochaine mesure
            time.sleep(30)  # Vérifier toutes les 30 secondes
            
    except KeyboardInterrupt:
        print("\nProgramme arrêté par l'utilisateur")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Nettoyage
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Déconnecté du broker MQTT")

if __name__ == "__main__":
    main()
