import json
import paho.mqtt.client as mqtt
from datetime import datetime

class MQTTClient:
    def __init__(self, broker, port, username, password, client_id="raspberry_pi_monitor"):
        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(username, password)
        self.broker = broker
        self.port = port
        self.connected = False
        
        # Configuration des callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        
        # Dictionnaire pour stocker les callbacks de topics
        self.topic_callbacks = {}
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connecté au broker MQTT {self.broker}")
            self.connected = True
            
            # Réabonnement aux topics
            for topic in self.topic_callbacks:
                self.client.subscribe(topic)
                print(f"Abonné à {topic}")
        else:
            print(f"Échec de la connexion avec le code: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        print(f"Déconnecté du broker MQTT. Raison: {rc}")
    
    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        if topic in self.topic_callbacks:
            payload = msg.payload.decode()
            self.topic_callbacks[topic](payload)
    
    def connect(self):
        """Se connecte au broker MQTT"""
        try:
            print(f"Connexion au broker {self.broker}...")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False
    
    def disconnect(self):
        """Déconnecte du broker MQTT"""
        self.client.loop_stop()
        self.client.disconnect()
        print("Déconnecté du broker MQTT")
    
    def publish(self, topic, message):
        """Publie un message sur un topic"""
        if isinstance(message, dict):
            message = json.dumps(message)
        
        result = self.client.publish(topic, message)
        if result.rc == 0:
            return True
        else:
            print(f"Erreur lors de la publication: {result.rc}")
            return False
    
    def subscribe(self, topic, callback):
        """S'abonne à un topic avec un callback associé"""
        self.topic_callbacks[topic] = callback
        
        # Configuration du callback de message
        if not self.client.on_message:
            self.client.on_message = self._on_message
        
        # S'abonner si déjà connecté
        if self.connected:
            self.client.subscribe(topic)
            print(f"Abonné à {topic}")
