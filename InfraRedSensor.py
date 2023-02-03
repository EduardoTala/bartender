import RPi.GPIO as GPIO
from Servo import Servo
import time

class IRSensor:
    
    # When there is no obstacles or object within the detection distance, 
    # the output is at HIGH position (5V or 3.3V). 
    # When the distance shorter than or equal to the threshold set, the output signal will change to position LOW (0V).
    
    def __init__(self, input_pin) -> None:
        # Setup pin layout on PI
        GPIO.setmode(GPIO.BCM)
        print(f"Setting up IR with pin : {input_pin}")
        self.input_pin = input_pin
        GPIO.setup(self.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def get_input(self):
        return GPIO.input(self.input_pin)



if __name__ == "__main__":
    ir = IRSensor(25)
    servo = Servo(12)
    
    try:
        
        while True:
            
            time.sleep(0.1)
            
            if (ir.get_input() == 0):
                print(ir.get_input())
                servo.move_90()
                time.sleep(1)
                servo.move_180()    
            
    except KeyboardInterrupt:
        print("User Keyboard Interrupt: ")
    finally:
        print("Cleaning GPIO and finishing script...")
        GPIO.cleanup()
        