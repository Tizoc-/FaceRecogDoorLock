import cv2
import os
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

'''Receive Arduino Signal'''
#GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN,)
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

'''Send Arduino Signal'''
#GPIO.setup(18,GPIO.OUT)

'''LED Control'''
#GPIO.setup(29,GPIO.OUT)#Green LED
#GPIO.setup(31,GPIO.OUT)#Red LED
'''Button Control'''
GPIO.setup(31,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
'''Servo Control'''
GPIO.setup(16,GPIO.OUT)
pwm = GPIO.PWM(16,25)
pwm.start(2)

#variable = 0;


def image_capture():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) 
    cam.set(4, 480) 
    cv2.imshow('img1',cam) #display the captured image     
            cv2.imwrite('images/c1.png',cam)
            cv2.destroyAllWindows()
            break
        cam.release()
        cv2.destroyAllWindows()
    return cam

def servo():

    pwm.ChangeDutyCycle(1)
    print("1\n")
    time.sleep(3);
    image_capture()
    pwm.ChangeDutyCycle(3)
    print("3\n")
    image_capture()
    time.sleep(3);
    pwm.ChangeDutyCycle(5)
    print("5\n")
    time.sleep(3)
    pwm.ChangeDutyCycle(3)
    print("end\n")
    time.sleep(3)
    image_capture()

def main():
    if(GPIO.input(15) == GPIO.HIGH):
        time.sleep(0.5)
       
    elif(GPIO.input(13) == GPIO.HIGH):
        time.sleep(0.5)
        servo()
    elif(GPIO.input(31) == GPIO.HIGH):
            time.sleep(0.5)
            pwm.ChangeDutyCycle(4)
            print("Unlock\n")
            time.sleep(5);
            pwm.ChangeDutyCycle(2)
            time.sleep(0.2)
    elif(GPIO.input(37) == GPIO.HIGH):
        return 1
    
            
while(1):
    main()
    if(main() == 1):
        pwm.stop()
        GPIO.cleanup()
        break

