import RPi.GPIO as GPIO

class HallSensor:
    
    def __init__(self, input_pin) -> None:
        self.input_pin = input_pin
        GPIO.setup( self.input_pin, GPIO.IN)