import cv2
import os
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO
import time

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(37, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an inputpin and set initial value to be pulled low (off)
GPIO.setup(16, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) 
while True: # Run forever
    if GPIO.input(37) == GPIO.HIGH:
        print("Button was pushed!")
        time.sleep(1)
    elif GPIO.input(16) == GPIO.HIGH:
        print("Btn was pushed!")
        time.sleep(1)
