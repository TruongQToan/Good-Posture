from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

import cv2
import numpy as np


class Camera(QObject):
    frame = pyqtSignal(np.ndarray)

    def __init__(self, camera_config):
        super(Camera, self).__init__(None)

        self._cap = None
        self._cam_num = camera_config.cam_num
        self._fps = camera_config.fps

        self._initialize()

    def _initialize(self):
        self._cap = cv2.VideoCapture(self._cam_num)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._get_frame)
        self._timer.setInterval(1000 // self._fps)
    
    @pyqtSlot()
    def _get_frame(self):
        _, frame = self._cap.read()
        return self.frame.emit(frame)

    def close_camera(self):
        self._cap.release()

    @property
    def paused(self):
        return not self._timer.isActive()

    @paused.setter
    def paused(self, p):
        if p:
            self._timer.stop()
        else:
            self._timer.start()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self._cam_num)
