import time
from datetime import datetime

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

def main():
    try:
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
            
            # Attendre avant la prochaine mesure
            time.sleep(5)  # Vérifier toutes les 5 secondes
            
    except KeyboardInterrupt:
        print("\nProgramme arrêté par l'utilisateur")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
