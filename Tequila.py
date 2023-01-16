#!/usr/bin/env python3
from time import sleep
import RPi.GPIO as GPIO
from StepperMotor import StepperMotor
from StopMotorInterrupt import StopMotorInterrupt
from LimitSensor import LimitSensor

from threading import Thread, Event

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

UP = True #Clockwise rotation
DOWN = False #Counter Clockwise rotation
SPR  = 800  # Steps per Revolution (360 / 0.45) NEMA 17 17HS4401S and 17HS40235 800 steps per rev

MAX_SPEED = 0.0001 #MAX SPEED supported by the motor, don't get any lower than this
MID_SPEED = 0.0005
MID_SLO_SPEED = 0.001
SLO_SPEED = 0.01

# create a shared event object
stop_motor_event = Event()

#Create a Motor object
motor = StepperMotor()

#LIMIT SENSOR CONFIGURATION
LIMIT_SENSOR_UP = 17  # Limit sensor UP pin
LIMIT_SENSOR_DOWN = 27 # Limit sensor DOWN pin

#Create limit objects
limit_up = LimitSensor(LIMIT_SENSOR_UP)
limit_down = LimitSensor(LIMIT_SENSOR_DOWN)

# define the event; bountime of 5mSec means that subsequent edges will be ignored for 5mSec
GPIO.add_event_detect(LIMIT_SENSOR_UP, GPIO.FALLING, callback=lambda x: limit_up(LIMIT_SENSOR_UP), bouncetime=5)
GPIO.add_event_detect(LIMIT_SENSOR_DOWN, GPIO.FALLING, callback=lambda x: limit_down(LIMIT_SENSOR_DOWN), bouncetime=5)

# Define Servo pin, PWM pin in raspberry
servo = 12

print("")
print("########### CONFIGURATION FINISHED #################")
print("")





#Function to detect if a limit switch was triggered
def limit_up(channel) -> None:
    sleep(0.005) # edge debounce of 5mSec
    # only deal with valid Falling edges
    if(GPIO.input(channel)==0):
        print("limit up reached")
        stop_motor_event.set()
        sleep(0.01)
        move_down = Thread(target=motor.move, args=(DOWN, SPR*50, MAX_SPEED, stop_motor_event), name="Moving DOWN")
        stop_motor_event.clear()
        move_down.start()
    return
    
    
#Function to detect if a limit switch was triggered
def limit_down(channel) -> None:
    sleep(0.005) # edge debounce of 5mSec
    # only deal with valid Falling edges
    if(GPIO.input(channel)==0):
        print("limit down reached")
        stop_motor_event.set()
        sleep(0.01)
        move_up = Thread(target=motor.move, args=(UP, SPR*50, MAX_SPEED, stop_motor_event), name="Moving UP")
        stop_motor_event.clear()
        move_up.start()
    return
    


def main():
    
    move = Thread(target=motor.move, args=(UP, SPR*50, MAX_SPEED, stop_motor_event), name="Start moving")
    move.start()
    
    try:

        while True:
            sleep(1)
            """             response = input("Up or Down?   ")
            if(response == "u"):
                motor.move(UP, SPR*100, MAX_SPEED)
                home = True
            else:
                motor.move(DOWN, SPR*100, MAX_SPEED)
                home = False """


        
    except KeyboardInterrupt:
        print("User Keyboard Interrupt: ")
    except StopMotorInterrupt:
        print("Stop Motor Interrupt in Tequila Class")
    except Exception as motor_error:
        print("Unexpected error in Tequila.py:" + str(motor_error))
    finally:
        print("Cleaning GPIO and finishing script...")
        GPIO.cleanup()
  

  
if __name__ == "__main__":
    main()