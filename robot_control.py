#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

from input_test import getch
from flask import Flask
from flask import request

# Initialize flask server app
# app = Flask(__name__)

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Definition of RGB module pins
LED_R = 22
LED_G = 27
LED_B = 24

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

# Car speed
SPEED = 20

#Define the servo pin
ServoPinF = 4 # Front
ServoPinH = 11 # Horizontal
ServoPinV = 9 # Vertical

# Initial Servo positions 
ServoPOSF = 90 # Front
ServoPOSH = 90 # Horizontal
ServoPOSV = 90 # Vertical

#Motor pin initialization operation
def motor_init():
    global pwm_ENA
    global pwm_ENB
    '''
    global pwm_servoF
    global pwm_servoH
    global pwm_servoV
    '''

    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    
    GPIO.setup(ServoPinF,GPIO.OUT)
    GPIO.setup(ServoPinH,GPIO.OUT) 
    GPIO.setup(ServoPinV,GPIO.OUT)

    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)

    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    
    '''
    pwm_servoF = GPIO.PWM(ServoPinF, 50)
    pwm_servoH = GPIO.PWM(ServoPinH, 50)
    pwm_servoV = GPIO.PWM(ServoPinV, 50)

    pwm_servoF.start(0)
    pwm_servoH.start(0)
    pwm_servoV.start(0)
    '''

#advance
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#back
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#turn left
def left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#turn right
def right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#turn left in place
def spin_left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#turn right in place
def spin_right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#brake
def brake(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED)
    pwm_ENB.ChangeDutyCycle(SPEED)
    time.sleep(delaytime)

#Define a pulse function to generate the PWM value in the analog mode. 
#The base pulse is 20ms, and the high level of the pulse is controlled at 0-180 degrees in 0.5-2.5ms.
def servo_pulse(myangle, ServoPin):
    pulsewidth = (myangle * 11) + 500
    GPIO.output(ServoPin, GPIO.HIGH)
    time.sleep(pulsewidth/1000000.0)
    GPIO.output(ServoPin, GPIO.LOW)
    time.sleep(20.0/1000-pulsewidth/1000000.0)

#Delay 2s	
time.sleep(2)

#The try/except statement is used to detect errors in the try block.
#the except statement catches the exception information and processes it.
#The robot car advance 1s，back 1s，turn left 2s，turn right 2s，turn left  in place 3s
#turn right  in place 3s，stop 1s。

# @app.route("/")
def main():
    global ServoPOSH
    global ServoPOSV
    global ServoPinH
    global ServoPinV
    while True:
        # motion = request.args.get('command')
        motion = getch()
        if motion == "w":
            run(0.5)
        elif motion == "s":
            back(0.5)
        elif motion == "a":
            left(0.1)
        elif motion == "d":
             right(0.1)
        elif motion == "q":
            spin_left(0.1)
        elif motion == b"e":
            spin_right(0.1)
        elif motion == "l":
            ServoPOSH = max(30, ServoPOSH - 10)
            servo_pulse(ServoPOSH, ServoPinH)
        elif motion == "j":
            ServoPOSH = min(150, ServoPOSH + 10)
            servo_pulse(ServoPOSH, ServoPinH)
        elif motion == "k":
            ServoPOSV = max(30, ServoPOSV - 10)
            servo_pulse(ServoPOSV, ServoPinV)
        elif motion == "i":
            ServoPOSV = min(150, ServoPOSV + 10)
            servo_pulse(ServoPOSV, ServoPinV)
        brake(0.01)
        if motion == "p":
            break
            # func = request.environ.get('werkzeug.server.shutdown')
            # print("shutting down server")
            #func()
    #except KeyboardInterrupt:
    #    pass
    #return "Hello world!"

if __name__ == '__main__':
    motor_init()
    # app.run()
    main()
    pwm_ENA.stop()
    pwm_ENB.stop()
    GPIO.cleanup() 

