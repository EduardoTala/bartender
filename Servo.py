import RPi.GPIO as GPIO
import time


# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms (1000ms/50 cycles per second)
# duty cycle for 0 degree     = (1ms/20ms)*100 = 5%  Left
# duty cycle for 90 degree    = (1.5ms/20ms)*100 = 7.5%  Neutral
# duty cycle for 180 degree   = (2ms/20ms)*100 = 10%  Right

#This is the theory but the values that worked better are 2% to 12%



#                 90°   
#         |----------------|
#         |        Shaft   |           <-- Orange - Signal 
#   180°  |           O--->|  0°       <-- Red - 5v                
#         |                |           <-- Brown - gnd
#         |----------------|
#
class Servo:
    
    def __init__(self, input_pin) -> None:
        # Setup pin layout on PI
        GPIO.setmode(GPIO.BCM)
        print(f"Setting up Servo with pin : {input_pin}")
        self.input_pin = input_pin
        GPIO.setup(self.input_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.input_pin,50)
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(2) # 0 deg position
        self.pwm.ChangeDutyCycle(0) #Avoid Jittering
        time.sleep(2)
        

    def move_0(self):
        print("Moving to 0 degrees, 2% DutyCycle")
        self.pwm.ChangeDutyCycle(2) # 0 deg position
        time.sleep(0.3)
        self.pwm.ChangeDutyCycle(0) #Avoid Jittering
        time.sleep(0.3)
        return
            
            
    def move_90(self):
        print("Moving to 90 degrees, 7% DutyCycle")
        self.pwm.ChangeDutyCycle(7) # 90 deg position
        time.sleep(0.3)
        self.pwm.ChangeDutyCycle(0) #Avoid Jittering
        time.sleep(0.3)
        return
    
    
    def move_180(self):
        print("Moving to 180 degrees, 12% DutyCycle")
        self.pwm.ChangeDutyCycle(12) # 180 deg position
        time.sleep(0.3)
        self.pwm.ChangeDutyCycle(0) #Avoid Jittering
        time.sleep(0.3)
        return
        
    def stop(self):
        self.pwm.stop()
        
    def cleanup(self):
        GPIO.cleanup()
        
        
    #Move servo to the serving position
    def serve(self) -> None:
        print("Changing to Serve position")
        self.pwm.ChangeDutyCycle(2)
        time.sleep(0.3)
        return
    
    #Move servo to the waiting position
    def wait(self) -> None:
        print("Changing to wait position")
        self.pwm.ChangeDutyCycle(12)
        time.sleep(0.3)
        return
    
    
if __name__ == "__main__":
    s = Servo(12)
    #s.move_0()
    time.sleep(1)
    s.move_90()
    time.sleep(1)
    s.move_180()
    time.sleep(1)
    s.move_0()
    s.move_180()
    time.sleep(1)
    s.stop()
    s.cleanup()