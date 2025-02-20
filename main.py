import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
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
MQTT_TOPIC = "test/topic"

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au broker avec le code: {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Abonné au topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message reçu: {message}")
    
    # Contrôle de la LED basé sur le message
    if message.lower() == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED allumée")
    elif message.lower() == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED éteinte")

def main():
    try:
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
        
        # Boucle principale
        while True:
            # Publie un message périodique
            client.publish(MQTT_TOPIC, "Hello depuis le Raspberry Pi!")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme")
        client.loop_stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()