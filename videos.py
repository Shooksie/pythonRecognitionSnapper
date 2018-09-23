import numpy as np
import datetime
import cv2
import copy

face_cascade = cv2.CascadeClassifier('C:\\Users\\shooks\\PycharmProjects\\camera.py\\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\\Users\\shooks\\PycharmProjects\\camera.py\\haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

facacialTimeStamp = dict()

captureCounter = 1
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    counter = 1
    for (x, y, w, h) in faces:
        crop_img = copy.deepcopy(frame[y:y + h, x:x + w])
        timeStamp = str(datetime.datetime.now()).split('.')[0].split(' ')
        timeStamp = '{}-{}'.format(timeStamp[0], timeStamp[1]).replace(':','-')
        if facacialTimeStamp.get(timeStamp):
            facacialTimeStamp [timeStamp] += 1
        else:
            facacialTimeStamp[timeStamp] = 1

        title = 'faces2/capture-{}-{}.jpg'.format(timeStamp,facacialTimeStamp[timeStamp])
        counter += 1
        print(cv2.imwrite(title, crop_img))
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)



        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # if len(faces):
    #     timeStamp = str(datetime.datetime.now()).split('.')[0].split(' ')
    #     timeStamp = ''.join(timeStamp)
    #     cv2.imwrite('captures/capture{}.png'.format(timeStamp), frame)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# for (key, value) in facacialTimeStamp.items():
#     for i, faux in enumerate(value['frames']):
#         #cv2.imshow('image'+str(i), faux)
#         print(faux)
#         print(value['times'])
#         title = 'faces/capture-{}-{}.jpg'.format(value['times'],i)
#         print(cv2.imwrite(title,faux))
# cv2.waitKey(0)

        #print('faces/capture{}-{}.png'.format(value['times'],i,))
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()