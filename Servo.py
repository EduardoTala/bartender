import RPi.GPIO as GPIO

class Servo:
    
    def __init__(self, input_pin) -> None:
        print(f"Setting up Servo with pin : {input_pin}")
        self.input_pin = input_pin
        GPIO.setup(self.input_pin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        self.servo = GPIO.PWM(self.input_pin,50)
        self.servo.start(0)
        
    #Move servo to the serving position
    def serve(self) -> None:
        self.servo.ChangeDutyCycle(0)
        return
    
    #Move servo to the waiting position
    def wait(self) -> None:
        self.servo.ChangeDutyCycle(angle)
        return