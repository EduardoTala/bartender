#!/usr/bin/env python3
import time 
import RPi.GPIO as GPIO

from StepperMotor import StepperMotor
from StopMotorInterrupt import StopMotorInterrupt
from HallSensor import HallSensor

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

DIR  = 22   # Direction -> GPIO Pin
STEP = 23   # Step -> GPIO Pin
CW   = True # Clockwise Rotation = True, Counterclockwise Rotation = False
SPR  = 200000  # Steps per Revolution (360 / 0.45) NEMA 17 17HS4401S 800 steps per rev

HALL_SENSOR_UP = 2
#HALL_SENSOR_2 = 3

MAX_SPEED = 0.0001
MID_SPEED = 0.0005
MID_SLO_SPEED = 0.001
SLO_SPEED = 0.01

hall_1 = HallSensor(HALL_SENSOR_UP)
motor = StepperMotor(DIR, STEP, CW)


def limit_up(channel, CW):
    
    print(f"Calling Limit up, GPIO : {channel}")
    motor.stop()
    time.sleep(0.5)
    CW = not CW
    motor.move(CW, SPR, MID_SLO_SPEED)

        
# add FALLING edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(HALL_SENSOR_UP, GPIO.FALLING, callback=limit_up, bouncetime=1000)

motor.move(CW, SPR, MID_SLO_SPEED)

GPIO.cleanup()