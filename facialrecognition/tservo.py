# 98:D3:41:FD:3E:BD - HC-05 #3
# 98:D3:41:FD:3E:79 - HC-05 #2
# 98:D3:C1:FD:41:10 - HC-05 #4
import cv2
import os
import numpy as np
from PIL import Image
from time import gmtime, strftime

import RPi.GPIO as GPIO
import time
import serial

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pic=0
'''Servo Control'''
GPIO.setup(16,GPIO.OUT)
pwm = GPIO.PWM(16,25)
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
   
def servo():
            pwm.ChangeDutyCycle(2)
            print("2\n")
            image_capture()
            time.sleep(2);
            
            pwm.ChangeDutyCycle(3)
            print("3\n")
            image_capture()
            time.sleep(2);
            
            pwm.ChangeDutyCycle(4)
            print("4\n")
            image_capture()
            time.sleep(2)
            
            pwm.ChangeDutyCycle(3)
            print("end\n")
            time.sleep(2)
            


btserial=serial.Serial("/dev/rfcomm0",baudrate=9600)
print("connected")
#btserial1=serial.Serial("/dev/rfcomm1",baudrate=9600)
try:
	print"in try"
	while 1:
		print "Waiting for text"
		data=btserial.readline() #<--
		print "Text received"
		print data
		#datanum=int(data)
		#ddata=dbtserial.readline()
		#print("Type: ",type(data))
		#print(datanum)
		#data1=input("enter")
		time.sleep(1)
		#if(datanum==1):
			#servo()
		#if(datanum==2):
				#image_capture()
		
except KeyboardInterrupt:
	print("Quit")
    
#while(1):

    
