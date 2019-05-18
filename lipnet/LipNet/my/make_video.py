import numpy as np
import cv2

cap = cv2.VideoCapture('trump3.mp4')
#cap = cv2.VideoCapture('trump-2018-08-29_14.05.25.mp4')


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output2.mp4',fourcc, 25.0, (360, 288))

i = 1
while(cap.isOpened()):
    ret, frame = cap.read()    
    if i < 76:
        if ret==True:
            # write the frame
            out.write(frame)

            cv2.imshow('frame',frame)
            i += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    else:
        print(i)
        break
        

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()