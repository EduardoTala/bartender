#!/usr/bin/env python3
import time 
import RPi.GPIO as GPIO

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

DIR  = 22   # Direction -> GPIO Pin
STEP = 23   # Step -> GPIO Pin
CW   = True # Clockwise Rotation = True, Counterclockwise Rotation = False
SPR  = 200  # Steps per Revolution (360 / 0.45) NEMA 17 17HS4401S 800 steps per rev

MAX_SPEED = 0.0004
MID_SPEED = 0.0009
MID_SLO_SPEED = 0.001
SLO_SPEED = 0.01

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

speed = MID_SLO_SPEED


for step in range(SPR):
  GPIO.output(STEP, GPIO.HIGH)
  time.sleep(speed)
  GPIO.output(STEP, GPIO.LOW)
  time.sleep(speed)

print("Cleaning GPIO and finishing script...")
GPIO.cleanup()