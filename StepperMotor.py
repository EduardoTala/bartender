#!/usr/bin/env python3
import sys
import time 
import RPi.GPIO as GPIO
from StopMotorInterrupt import *

class StepperMotor:
    
    # Microstep Resolution
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}
    
    
    def __init__(self, dir_pin, step_pin, CW=True):
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.CW = CW # Clockwise Rotation = True, Counterclockwise Rotation = False
        
        #Signal to stop the motor
        self.stop_motor = False
        
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        
        GPIO.output(self.dir_pin, self.CW)
        
        #init delay for the motor
        time.sleep(0.5)
        
    
    def move(self, dir, steps, speed):
        print(f"Moving motor CW: {dir}, steps: {steps}, speed: {speed}")
        time.sleep(0.2)
        GPIO.output(self.dir_pin, dir)
        
        try:
            
            for x in range(steps):
                
                if self.stop_motor:
                    print(f"Stopped at step : {x}")
                    #raise StopMotorInterrupt()
                    return
                
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(speed)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(speed)
                
        except KeyboardInterrupt:
            print("User Keyboard Interrupt: ")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt in StepperMotor Class")
        except Exception as motor_error:
            print("Unexpected error:" + str(motor_error))


            
            
    
    def stop(self):
        print("Stop motor Class Function...")
        self.stop_motor = True
    
        
    def __repr__(self):
        return f"Motor DIR_PIN: ({self.dir_pin}, STEP_PIN: {self.step_pin})"
    
    def __str__(self):
        return f"Motor DIR_PIN: ({self.dir_pin}, STEP_PIN: {self.step_pin})"