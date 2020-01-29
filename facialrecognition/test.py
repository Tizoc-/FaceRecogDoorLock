import cv2
import sys
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)
video_capture.set(3,640) # set Width
video_capture.set(4,480) # set Height
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
## test
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        #roi_color = gray[y:y+h, x:x+w]  
    # Display the resulting frame
    cv2.imshow('Video', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
