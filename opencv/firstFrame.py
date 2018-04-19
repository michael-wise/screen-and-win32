import numpy as np
import cv2

#img = cv2.imread('C:\Users\Michael\Downloads\2015-08-14 00_47_56-.png',0)
#cv2.imshow('image',img)


cap = cv2.VideoCapture('C:\Users\Michael\Downloads\test_input.mp4')
print cap.isOpened()
#fourcc= cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc,20.00,(640,480))
while cap.isOpened():
    ret,frame = cap.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame',gray)
    if cv2.waitkey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows