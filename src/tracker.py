import numpy as np
import numpy.random as rnd
import cv2
import obj 
import os
import math

def find_best_contour(tracked_obj, contours):

    min_dist = -1 
    best_contour = contours[0]
    for i in range(len(contours)):
        # Find contour's centriod
        moment = cv2.moments(contours[i])
        if moment['m00'] == 0:
            moment['m00'] = 0.000001
        cx = int(moment['m10']/moment['m00'])
        cy = int(moment['m01']/moment['m00'])
        dist = int(np.sqrt((tracked_obj.cx - cx)**2 + (tracked_obj.cy - cy)**2))
        area = cv2.contourArea(contours[i])
        if (area >= tracked_obj.min_size) and (area < tracked_obj.max_size):
            if (dist < min_dist) or (min_dist == -1):
                best_contour = contours[i]
                min_dist = dist
    return best_contour, min_dist

def paint_frame(frame, dog, robot, show_trail, show_boxes, show_distance):

    if show_trail == 1:
        dog.print_trail(frame)
        robot.print_trail(frame)
    if show_boxes == 1:
        dog.box(frame)
        robot.box(frame)
    if show_distance == 1:
        cv2.line(frame, (dog.cx, dog.cy), (robot.cx, robot.cy), (255, 0, 0), 2)
        dist = int(np.sqrt((dog.cx - robot.cx)**2 + (dog.cy - robot.cy)**2))
        dist_loc = (int(np.shape(frame)[1]/10),int(np.shape(frame)[0]/10))
        cv2.putText(frame, 'Distance:' + str(dist), dist_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def track(fn, output_dir, dog_min, dog_max, robot_min, robot_max):

    # Initialize parameters
    video = cv2.VideoCapture(fn)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    dog = obj.Obj((0, 0), 'becky', dog_min, dog_max)
    robot = obj.Obj((0, 0), 'robot', robot_min, robot_max)

    # Capture frame-by-frame
    ret, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find a file name that isn't taken
    i = 1
    while os.path.isfile('%s%s%d%s' % (output_dir, '/result', i, '.mp4')):
        i = i + 1
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    frame_size = (np.shape(frame)[1], np.shape(frame)[0])
    new_video = cv2.VideoWriter('%s%s%d%s' % (output_dir, '/result', i, '.mp4'), fourcc, 20.0, frame_size)

    # Initialize interrupting parameters
    show_trail = 0
    show_boxes = 0
    show_distance = 0

    while(True):
        # Apply Background Subtraction
        fgmask = fgbg.apply(frame)
        fgmask = cv2.GaussianBlur(fgmask, (35, 35), 0)

        # Find object contours
        _, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

        if len(contours) != 0:
            best_contour, min_dist = find_best_contour(dog, contours)
            if min_dist != -1:
                moment = cv2.moments(best_contour)
                if moment['m00'] == 0:
                    moment['m00'] = 0.000001
                dog.cx = int(moment['m10']/math.ceil(moment['m00']))
                dog.cy = int(moment['m01']/math.ceil(moment['m00']))
                measure = np.array([[np.float32(dog.cx)], [np.float32(dog.cy)]])
                # Correct Measurements
                dog.kalman.correct(measure)
                dog.x, dog.y, dog.w, dog.h = cv2.boundingRect(best_contour)

        # Predict and show results.
        pred = dog.kalman.predict()
        dog.cx , dog.cy = pred[0], pred[1]
        dog.update_path((dog.cx, dog.cy))

        if len(contours) != 0:
            best_contour, min_dist = find_best_contour(robot, contours)
            if min_dist != -1:
                moment = cv2.moments(best_contour)
                if moment['m00'] == 0:
                    moment['m00'] = 0.000001
                robot.cx = int(moment['m10']/moment['m00'])
                robot.cy = int(moment['m01']/moment['m00'])
                measure = np.array([[np.float32(robot.cx)], [np.float32(robot.cy)]])
                # Correct Measurements
                robot.kalman.correct(measure)
                robot.x, robot.y, robot.w, robot.h = cv2.boundingRect(best_contour)

        # Predict and show results.
        pred = robot.kalman.predict()
        robot.cx , robot.cy = pred[0], pred[1]
        robot.update_path((robot.cx, robot.cy))

        # Display the resulting frame
        disp_frame = frame.copy()
        paint_frame(disp_frame, dog, robot, show_trail, show_boxes, show_distance)
        cv2.imshow('frame', cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGB))
        #cv2.imshow('frame', fgmask)

        key = cv2.waitKey(60) & 0xFF
        if key == ord('t'):
            show_trail = 1 - show_trail
        elif key == ord('b'):
            show_boxes = 1 - show_boxes
        elif key == ord('d'):
            show_distance = 1 - show_distance
        elif key == ord(' '):
            key = '0'
            while key != ord(' ') and key != ord('q'):
                if key == ord('q'):
                    break
                elif key == ord('t'):
                    show_trail = 1 - show_trail
                elif key == ord('b'):
                    show_boxes = 1 - show_boxes
                elif key == ord('d'):
                    show_distance = 1 - show_distance
                disp_frame = frame.copy()
                paint_frame(disp_frame, dog, robot, show_trail, show_boxes, show_distance)
                cv2.imshow('frame', cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGB))
                key = cv2.waitKey(0)
        if key == 27: #Esc ASCII code
            break
        key = '0'

        # Save frame to video
        paint_frame(disp_frame, dog, robot, 1, 1, 1)
        new_video.write(cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGB))

        # Capture frame-by-frame
        ret, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # When everything is done, release the capture
    video.release()
    new_video.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    track('../videos/ana.mp4', 20000, 1000000, 5000, 9000)