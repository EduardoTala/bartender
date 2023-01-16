import RPi.GPIO as GPIO

class LimitSensor:
    
    def __init__(self, input_pin) -> None:
        print(f"Setting up limit sensor with pin : {input_pin}")
        self.input_pin = input_pin
        GPIO.setup( self.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)