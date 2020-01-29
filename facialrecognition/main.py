
import RPi.GPIO as GPIO
import cv2
from nanpy import (ArduinoApi, SerialManager,Lcd)
from time import gmtime, strftime, sleep
import time 
import serial
# 98:D3:41:FD:3E:BD - HC-05 #3
# 98:D3:41:FD:3E:79 - HC-05 #2
# 98:D3:61:FD:41:79 - HC-05 #1
# /dev/ttyACM1 - Arduino USB Serial
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

'''Servo Control'''
GPIO.setup(12,GPIO.OUT)
pwm = GPIO.PWM(12,25)
#pwm.start(3)

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
   
def servo():
	image_capture()
	pwm.start(3)
	pwm.ChangeDutyCycle(2)
	print("2\n")
	image_capture()
	time.sleep(1);
	
	pwm.ChangeDutyCycle(3)
	print("3\n")
	image_capture()
	time.sleep(1);
	
	pwm.ChangeDutyCycle(4)
	print("4\n")
	image_capture()
	time.sleep(1)
	
	pwm.ChangeDutyCycle(3)
	print("end\n")
	time.sleep(2)
	pwm.stop()
def main():
    btserial=serial.Serial("/dev/rfcomm0",baudrate=9600)
    while 1:
        ''' Arduino next to entry point '''
        package = btserial.readline()
        print(package)
        ''' Detect New Package '''
        if(int(package)==1):
			pwm.stop()
			image_capture()
			time.sleep(3)
			pwm.start(2)
        ''' Detect Missing Package '''
        if(int(package)==2):
			servo()

main()
