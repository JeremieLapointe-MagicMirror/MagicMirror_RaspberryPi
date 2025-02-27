import RPi.GPIO as GPIO #Fonctionne seulement sur le raspberry pi
import paho.mqtt.client as mqtt #Fonctionne seulement sur le raspberry pi
import time

# Configuration GPIO
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Configuration MQTT
MQTT_BROKER = "mirrormqtt.jeremielapointe.ca"
MQTT_PORT = 1883
MQTT_USER = "MirrorMQTT"
MQTT_PASSWORD = "Patate123"
MQTT_STATUS_TOPIC = "led/status"

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au broker avec le code: {rc}")

def set_led_state(client, state):
    GPIO.output(LED_PIN, state)
    status_message = "ON" if state else "OFF"
    client.publish(MQTT_STATUS_TOPIC, status_message)
    print(f"LED {status_message}")

def main():
    try:
        # Création du client MQTT
        client = mqtt.Client()
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        
        # Attribution des callbacks
        client.on_connect = on_connect
        
        # Connexion au broker
        print(f"Connexion au broker {MQTT_BROKER}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Démarrage de la boucle MQTT
        client.loop_start()
        
        # État initial de la LED
        led_state = False
        
        # Boucle principale
        while True:
            # Change l'état de la LED
            led_state = not led_state
            set_led_state(client, led_state)
            
            # Attend 5 secondes
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme")
        client.loop_stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()