import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

'''Button Control'''
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

'''LED Control
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)'''

'''Servo Control'''
GPIO.setup(16,GPIO.OUT)
pwm = GPIO.PWM(16,25)
pwm.start(2)

variable = 0;

while GPIO.input(13) != GPIO.HIGH:
    input_state = GPIO.input(15)
    input_state2 = GPIO.input(13)
    if GPIO.input(15) == GPIO.HIGH:
        variable = variable + 1
        time.sleep(0.2);
        
    if variable % 2 == 1:
        pwm.ChangeDutyCycle(2.00)
        print("Lock\n")
        #GPIO.input(13) == GPIO.HIGH
        time.sleep(0.2);
    elif variable % 2 == 0:
        pwm.ChangeDutyCycle(4)
        print("Unlock\n")
        #GPIO.input(11) == GPIO.HIGH
        time.sleep(0.2);
        
pwm.stop()
GPIO.cleanup()
        