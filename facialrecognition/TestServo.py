import RPi.GPIO as GPIO
import cv2
from nanpy import (ArduinoApi, SerialManager,Lcd)
from time import gmtime, strftime, sleep
import time 
import serial

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12,GPIO.OUT)
pwm = GPIO.PWM(12,25)
pwm.start(3)

def image_capture():
    dump_frames=30
    cam = cv2.VideoCapture(0)
    for i in range(dump_frames):
        retval, img=cam.read()
        temp=img
    retval, img=cam.read()
    camera=img
    pictime=strftime("%a,%d%b%Y%X", gmtime())
    print(pictime)
    file = "/home/pi/dexcampics/"+pictime+".png"
    cv2.imwrite(file, camera)
    cam.release()
    cv2.destroyAllWindows()

def main():
	while True:
            cyc=input()
            if float(cyc) == -1:
                pwm.stop()
            elif float(cyc) == -2:
				pwm.stop()
				image_capture()
				time.sleep(3)
				pwm.start(2)
            else:
                pwm.ChangeDutyCycle(float(cyc))
                time.sleep(2)
main()
