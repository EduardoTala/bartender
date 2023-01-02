#!/usr/bin/env python3
import time 
import tty, sys, termios
import RPi.GPIO as GPIO

from threading import Thread, Event

from StepperMotor import StepperMotor
from StopMotorInterrupt import StopMotorInterrupt
from HallSensor import HallSensor

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

DIR  = 22   # Direction -> GPIO Pin
STEP = 23   # Step -> GPIO Pin
CW   = True # Clockwise Rotation = True, Counterclockwise Rotation = False
SPR  = 800  # Steps per Revolution (360 / 0.45) NEMA 17 17HS4401S 800 steps per rev

HALL_SENSOR_UP = 17
#HALL_SENSOR_2 = 3

MAX_SPEED = 0.0001
MID_SPEED = 0.0005
MID_SLO_SPEED = 0.001
SLO_SPEED = 0.01

hall_1 = HallSensor(HALL_SENSOR_UP)
motor = StepperMotor(DIR, STEP, CW)

#Function to detect if a limit switch was triggered
def limit_up(channel, CW):
    print(f"Calling Limit up, GPIO : {channel}, direction {CW}")
    motor.stop()


        
# add FALLING edge detection on a channel, ignoring further edges for 500ms for switch bounce handling
GPIO.add_event_detect(HALL_SENSOR_UP, GPIO.FALLING, callback=lambda x: limit_up(HALL_SENSOR_UP, CW), bouncetime=2000)

#motor.move(CW, SPR*2, SLO_SPEED)
#motor.move(not CW, SPR, MID_SLO_SPEED)
#motor.move(CW, SPR, MID_SPEED)
#motor.move(not CW, SPR, MAX_SPEED)
#motor.move(CW, SPR*2, MID_SLO_SPEED)

current_speed = MAX_SPEED
steps = int(SPR/4)

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
x = 0

try:
  
  while True:
    
    x=sys.stdin.read(1)[0]
    
    match x:
      case "w":
        print("Increase speed")
        current_speed = current_speed/3
        motor.move(CW, steps, current_speed)
      case "s":
        print("Decrease speed")      
        current_speed = current_speed*3
        motor.move(CW, steps, current_speed)
      case "d":
        print("CW")
        motor.move(CW, steps, current_speed)
      case "a": 
        print("CCW")
        motor.move((not CW), steps, current_speed)
        
        
except KeyboardInterrupt:
    print("User Keyboard Interrupt: ")
except StopMotorInterrupt:
    print("Stop Motor Interrupt in StepperMotor Class")
except Exception as motor_error:
    print("Unexpected error in Teuquila.py:" + str(motor_error))
    
finally:
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors) 
  print("Cleaning GPIO and finishing script...")
  GPIO.cleanup()