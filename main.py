import RPi.GPIO as GPIO
import time

LED_PIN = 18  # BCM pin 18

def main():
    # Configuration du GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    print("Test de la LED sur GPIO18")
    print("Ctrl+C pour arrêter")
    
    try:
        while True:
            # Allume la LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED ON")
            time.sleep(1)
            
            # Éteint la LED
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED OFF")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgramme arrêté")
        GPIO.cleanup()  # Nettoyage des GPIO

if __name__ == "__main__":
    main()