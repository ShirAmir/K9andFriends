import numpy as np
import numpy.random as rnd
import cv2
import obj 

VIDEO = r'../videos/ana.mp4'

if __name__ == "__main__":

    # Initialize parameters
    video = cv2.VideoCapture(VIDEO)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    dog = obj.Obj((0, 0), 'becky', 20000, 1000000)
    robot = obj.Obj((0, 0), 'robot', 5000, 9000)

    # Initialize interrupting parameters
    show_trail = 0
    show_boxes = 0
    show_distance = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Apply Background Subtraction
        fgmask = fgbg.apply(frame)
        fgmask = cv2.GaussianBlur(fgmask, (45, 45), 0)

        # Find object contours
        _, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) >= dog.min_size:
                # Find contour's centriod
                moment = cv2.moments(contours[i])
                dog.cx = int(moment['m10']/moment['m00'])
                dog.cy = int(moment['m01']/moment['m00'])
                # for debug -- show centriod
                if show_trail == 1:
                    cv2.circle(frame, (dog.cx, dog.cy), 6, (255, 0, 0), -1)
                measure = np.array([[np.float32(dog.cx)], [np.float32(dog.cy)]])
                # Correct Measurements
                dog.kalman.correct(measure)
                dog.x, dog.y, dog.w, dog.h = cv2.boundingRect(contours[i])
                break

        # Predict and show results.
        pred = dog.kalman.predict()
        dog.cx , dog.cy = pred[0], pred[1]
        dog.update_path((dog.cx, dog.cy))
        if show_trail == 1:
            dog.print_trail(frame)
        if show_boxes == 1:
            dog.box(frame)

        for i in range(len(contours)):
            if (cv2.contourArea(contours[i]) >= robot.min_size) and (cv2.contourArea(contours[i]) < robot.max_size):
                # Find contour's centriod
                moment = cv2.moments(contours[i])
                robot.cx = int(moment['m10']/moment['m00'])
                robot.cy = int(moment['m01']/moment['m00'])
                # for debug -- show centriod
                if show_trail == 1:
                    cv2.circle(frame, (robot.cx, robot.cy), 6, (255, 0, 0), -1)
                measure = np.array([[np.float32(robot.cx)], [np.float32(robot.cy)]])
                # Correct Measurements
                robot.kalman.correct(measure)
                robot.x, robot.y, robot.w, robot.h = cv2.boundingRect(contours[i])
                break

        # Predict and show results.
        pred = robot.kalman.predict()
        robot.cx , robot.cy = pred[0], pred[1]
        robot.update_path((robot.cx, robot.cy))
        if show_trail == 1:
            robot.print_trail(frame)
        if show_boxes == 1:
            robot.box(frame)
        
        if show_distance == 1:
            cv2.line(frame, (dog.cx, dog.cy), (robot.cx, robot.cy), (255, 0, 0), 2)
            dist = int(np.sqrt((dog.cx - robot.cx)**2 + (dog.cx - robot.cx)**2))
            dist_loc = (int(np.shape(frame)[1]/10),int(np.shape(frame)[0]/10))
            cv2.putText(frame, 'Distance:' + str(dist), dist_loc, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #cv2.imshow('frame', fgmask)

        key = cv2.waitKey(60) & 0xFF 
        if key == ord('q'):
            break
        elif key == ord('p'):
            key = '0'
            while key != ord('p'):
                key = cv2.waitKey(0)
        elif key == ord('t'):
            show_trail = 1 - show_trail
        elif key == ord('b'):
            show_boxes = 1 - show_boxes
        elif key == ord('d'):
            show_distance = 1 - show_distance
        key = '0'

    # When everything is done, release the capture
    video.release()
    cv2.destroyAllWindows()