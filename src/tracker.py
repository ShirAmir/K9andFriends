# *************************************************
# ********** Multi Object Motion Tracker **********
# ************ Merav Joseph 200652063 *************
# ************* Shir Amir 209712801 ***************
# *************************************************

import numpy as np
import numpy.random as rnd
import cv2
import obj 

VIDEO = r'../videos/ana.mp4'
RECT_WIDTH = 30
RECT_HEIGHT = 20

# Initialize parameters
video = cv2.VideoCapture(VIDEO)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
dog = obj.Obj((0,0), 'bucky', 20000, 1000000)
robot = obj.Obj((0,0), 'robot', 5000, 9000)
x_dog, y_dog, w_dog, h_dog = (0,0,0,0)
x_robot, y_robot, w_robot, h_robot= (0,0,0,0)

while(True):
    # Capture frame-by-frame
    ret, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply Background Subtraction
    fgmask = fgbg.apply(frame)
    fgmask = cv2.GaussianBlur(fgmask,(45,45),0)

    # Find object contours
    _, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) >= dog.min_size:
            # Find contour's centriod
            moment = cv2.moments(contours[i])
            cx = int(moment['m10']/moment['m00'])
            cy = int(moment['m01']/moment['m00'])
            # for debug -- show centriod
            cv2.circle(frame, (cx, cy), 6, (255, 0, 0), -1)
            measure = np.array([[np.float32(cx)], [np.float32(cy)]])
            # Correct Measurements
            dog.kalman.correct(measure)
            x_dog, y_dog, w_dog, h_dog = cv2.boundingRect(contours[i])
            break

    # Predict and show results.
    pred = dog.kalman.predict()
    cx , cy = pred[0], pred[1]
    dog.update_path((cx, cy))
    for point in dog.path:
        cv2.circle(frame, point, 3, dog.color, -1)
    cv2.rectangle(frame, (x_dog, y_dog), (x_dog+w_dog, y_dog+h_dog), dog.color, 2)
    cv2.putText(frame, dog.__str__(), (x_dog, y_dog+h_dog+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, dog.color, 2)

    for i in range(len(contours)):
        if (cv2.contourArea(contours[i]) >= robot.min_size) and (cv2.contourArea(contours[i]) < robot.max_size):
            # Find contour's centriod
            moment = cv2.moments(contours[i])
            cx = int(moment['m10']/moment['m00'])
            cy = int(moment['m01']/moment['m00'])
            # for debug -- show centriod
            cv2.circle(frame, (cx, cy), 6, (255, 0, 0), -1)
            measure = np.array([[np.float32(cx)], [np.float32(cy)]])
            # Correct Measurements
            robot.kalman.correct(measure)
            x_robot, y_robot, w_robot, h_robot = cv2.boundingRect(contours[i])
            break

    # Predict and show results.
    pred = robot.kalman.predict()
    cx , cy = pred[0], pred[1]
    robot.update_path((cx, cy))
    for point in robot.path:
        cv2.circle(frame, point, 3, robot.color, -1)
    cv2.rectangle(frame, (x_robot, y_robot), (x_robot+w_robot, y_robot+h_robot), robot.color, 2)
    cv2.putText(frame, robot.__str__(), (x_robot, y_robot+h_robot+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, robot.color, 2)

    # Display the resulting frame
    cv2.imshow('frame', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #cv2.imshow('frame', fgmask)
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break

# When everything done, release the capture
video.release()
cv2.destroyAllWindows()