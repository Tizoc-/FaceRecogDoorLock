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
face_id=2

recognizer = cv2.face.LBPHFaceRecognizer_create()
font = cv2.FONT_HERSHEY_SIMPLEX
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def image_capture(face_id):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) 
    cam.set(4, 480) 
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    
    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff 
        if k == 27:
            break
        elif count >= 10:
            break
    if(face_id==9):
        face_id=2
    else:
        face_id=face_id+1
    
    cam.release()
    cv2.destroyAllWindows()

def get_samples(path):
    
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    face_samples=[]
    ids=[]
    for imagePath in imagePaths:
        pImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces=face_detector.detectMultiScale(imageNp)
        for (x,y,w,h) in faces:
            face_samples.append(imageNp[y:y+h,x:x+w])
            ids.append(Id)
    return face_samples,ids
def servo(lock):
    while (lock ==True or lock ==False):
        
        if(lock==False):
            pwm.ChangeDutyCycle(2.00)
            print("Lock\n")
            time.sleep(0.2);
            break
        elif(lock):
            time.sleep(0.5)
            pwm.ChangeDutyCycle(4)
            print("Unlock\n")
            time.sleep(5);
            pwm.ChangeDutyCycle(2)
            time.sleep(0.2)
            break
    
'''
def feature_recognizer():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #face_detector.load('trainner/trainner.yml')
    Id=0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf<50):
                return True
                if(Id==1):
                    Id="Paul"
                elif(Id==2):
                    Id="Other"
            else:
                return False
            
                
                #cv2.imshow('image', img)
            cv2.putText(img, str(Id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.imshow('video',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cam.release()
    cv2.destroyAllWindows()
'''
def pic_recognizer():
    dump_frames=30
    Id=0
    conf=0
    cam=cv2.VideoCapture(0)
    for i in range(dump_frames):
        retval, img=cam.read()
        temp=img
    retval, img=cam.read()
    camera=img
    file = "/home/pi/test_image.png"
    cv2.imwrite(file, camera)
    image=cv2.imread(file)
    #cv2.imshow("Faces found", image)
    gray =cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
    print(conf)
    print(Id)
    if(conf<50):
        if(Id>0):           
            cam.release()
            cv2.destroyAllWindows()
            return True
        else:
            cam.release()
            cv2.destroyAllWindows()
            return False
            
    else:
       
        cam.release()
        cv2.destroyAllWindows()
        return False
    
    
    cam.release()
    cv2.destroyAllWindows()
    
    

def main():
    if(GPIO.input(15) == GPIO.HIGH):
        time.sleep(0.5)
        image_capture(face_id)
        faceSamples, ids = get_samples('dataset')
        recognizer.train(faceSamples,np.array(ids))
        recognizer.save('trainer/trainner.yml')
    elif(GPIO.input(13) == GPIO.HIGH):
        time.sleep(0.5)
        faceSamples, ids = get_samples('dataset')
        recognizer.train(faceSamples,np.array(ids))
        recognizer.save('trainer/trainner.yml')
        ##lock=feature1_recognizer()
        lock=pic_recognizer()
        print(lock)
        servo(lock)
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
