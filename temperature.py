import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Configuration MQTT
MQTT_BROKER = "broker.hivemq.com"  # Remplacez par l'adresse de votre broker
MQTT_PORT = 1883
MQTT_TOPIC = "raspberry/temperature"  # Sujet où publier les données
MQTT_CLIENT_ID = "raspberry_pi_temp_monitor"

# Fonction pour obtenir la température du CPU
def get_cpu_temperature():
    try:
        # Ouvrir le fichier contenant la température
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0  # Convertir en degrés Celsius
        return temp
    except Exception as e:
        print(f"Erreur lors de la lecture de la température: {e}")
        return None

# Callback lors de la connexion au broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT")
    else:
        print(f"Échec de la connexion avec le code: {rc}")

# Créer un client MQTT
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.on_connect = on_connect

# Connexion au broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    # Boucle principale
    while True:
        # Obtenir la température
        temperature = get_cpu_temperature()
        
        if temperature is not None:
            # Créer un message avec la température et l'horodatage
            message = {
                "temperature": temperature,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "device": "raspberry_pi_4"
            }
            
            # Convertir en JSON et publier
            payload = json.dumps(message)
            client.publish(MQTT_TOPIC, payload)
            
            print(f"Température publiée: {temperature}°C")
        
        # Attendre avant la prochaine mesure
        time.sleep(60)  # Publier toutes les minutes

except KeyboardInterrupt:
    print("Programme arrêté par l'utilisateur")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"Erreur: {e}")
    client.loop_stop()
    client.disconnect()
