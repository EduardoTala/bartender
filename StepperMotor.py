#!/usr/bin/env python3
import time 
import RPi.GPIO as GPIO
from StopMotorInterrupt import *

from threading import Event

class StepperMotor:
    
    # Microstep Resolution ONLY FOR GUIDANCE SINCE WE ARE USING A Shield Expansión Driver Drv8825, WE SET THESE ON THE PHISICAL SWITCHES
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}
    
    
    def __init__(self, dir_pin, step_pin):
        
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.stop_flag = False
        
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        
        print(f"Motor configuration DIR_PIN: {self.dir_pin}, STEP_PIN: {self.step_pin}")
        
        #init delay for the motor
        time.sleep(0.5)
        
        
        
        

    def move(self, dir, steps, speed, event_stop) -> None:
        
        print(f"Moving motor UP: {dir}, steps: {steps}, speed: {speed}")
        GPIO.output(self.dir_pin, dir)
                
        try:
           
            for x in range(steps):
                
                if event_stop.is_set():
                    print(f"Stopped at step : {x}")
                    self.stop_flag = False
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
        self.stop_flag = True


        
    def __repr__(self) -> str :
        return f"Motor configuration DIR_PIN: ({self.dir_pin}, STEP_PIN: {self.step_pin})"
    
    def __str__(self) -> str :
        return f"Motor configuration DIR_PIN: ({self.dir_pin}, STEP_PIN: {self.step_pin})"