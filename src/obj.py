import numpy as np
import numpy.random as rnd
import cv2

STATE_NUM = 4
MEASURE_NUM = 2


class Obj:
    max_path_length = 10

    def __init__(self, start_point, name, min_thresh, max_thresh):
        # The object's kalman tracker
        self.kalman = cv2.KalmanFilter(STATE_NUM, MEASURE_NUM)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
                                                np.float32)
        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                                               np.float32) * 0.3
        # The object's unique identifier
        self.id = name

        # The object's contour size boundaries
        self.max_size = max_thresh
        self.min_size = min_thresh 

        # The object's associated color
        self.color = (rnd.randint(255), rnd.randint(255), rnd.randint(255))

        # The object's path
        self.path = [start_point]

        # The object's bounding box
        self.x, self.y, self.w, self.h = (0, 0, 0, 0)

        # The object's Centriod
        self.cx, self.cy = (0, 0)

    def update_path(self, path_point):
        if len(self.path) == Obj.max_path_length:
            del self.path[0]
        self.path.append(path_point)

    def __str__(self):
        return str(self.id)

    def box(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, 2)
        cv2.putText(frame, self.__str__(), (self.x, self.y + self.h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color, 2)

    def print_trail(self, frame):
        for point in self.path:
            cv2.circle(frame, point, 3, self.color, -1)
