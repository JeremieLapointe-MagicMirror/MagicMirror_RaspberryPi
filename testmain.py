from gpiozero import MotionSensor

pir = MotionSensor(4)

while True:
    print("Continue scanning for human presence")
    pir.wait_for_motion()

    print("Human detected")
    pir.wait_for_no_motion()

    print("Human left")
