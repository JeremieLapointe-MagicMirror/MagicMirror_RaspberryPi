import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration MQTT
MQTT_CONFIG = {
    'broker': os.getenv('MQTT_BROKER'),
    'port': int(os.getenv('MQTT_PORT', 1883)),
    'username': os.getenv('MQTT_USERNAME'),
    'password': os.getenv('MQTT_PASSWORD'),
    'topic_temperature': os.getenv('MQTT_TOPIC_TEMPERATURE', 'serial/temperature'),
    'topic_pir_state': os.getenv('MQTT_TOPIC_PIR_STATE', 'serial/etatpir'),
    'topic_led_command': os.getenv('MQTT_TOPIC_LED_COMMAND', 'led/command'),
    'topic_led_status': os.getenv('MQTT_TOPIC_LED_STATUS', 'led/status'),
}

# Configuration des capteurs
SENSOR_CONFIG = {
    'temperature_check_interval': 30,  # secondes
    'motion_pin': 23,  # GPIO pin pour le capteur PIR
    'touch_pin': 17,
}

# Configuration des LEDs
LED_CONFIG = {
    'pin': 18,
    'num_pixels': 35,
    'brightness': 0.1,
    'colors': {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (255, 0, 255),
        'cyan': (0, 255, 255),
        'white': (255, 255, 255),
        'off': (0, 0, 0),
    }
}