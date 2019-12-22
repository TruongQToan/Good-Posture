from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QTabWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QTextEdit, QDialog)

import cv2 as cv
import numpy as np

from models import Camera
from config import Config


class ImageView(QWidget):
    def __init__(self, camera):
        super(ImageView, self).__init__(None)

        self._image_frame = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self._image_frame)
        self.setLayout(layout)
        self._camera = camera

        self._camera.frame.connect(self._show_frame)
    
    @pyqtSlot(np.ndarray)
    def _show_frame(self, frame):
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(image).scaled(720, 480, Qt.KeepAspectRatio)
        self._image_frame.setPixmap(pixmap)


class MainWindow(QDialog):
    def __init__(self, camera, config):
        super(MainWindow, self).__init__(None)

        self._camera = camera
        layout = QVBoxLayout()
        layout.addWidget(self.createTabWidget())
        self.setLayout(layout)
        self.setWindowTitle("Good Posture")

    def createTabWidget(self):
        tabWidget = QTabWidget()
        tabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        tab1 = QWidget()

        tab1_layout = QVBoxLayout()
        tab1_layout.setAlignment(Qt.AlignTop)
        image_view = ImageView(self._camera)
        self.resize(image_view.width(), image_view.height())
        label = QLabel(self)
        label.setText("Please sit with proper posture and use the preview to set posture baseline")
        label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        tab1_layout.addWidget(image_view)
        tab1_layout.addWidget(label)
        tab1.setLayout(tab1_layout)
        tab2 = QWidget()

        textEdit = QTextEdit()
        textEdit.setPlainText("Twinkle, twinkle, little star")
        tab2_layout = QHBoxLayout()
        tab2_layout.addWidget(textEdit)
        tab2.setLayout(tab2_layout)
        tabWidget.addTab(tab1, "General")
        tabWidget.addTab(tab2, "Notification")
        return tabWidget


if __name__ == '__main__':
    import sys

    config = Config()
    camera = Camera(config.camera_config)

    app = QApplication(sys.argv)
    camera.paused = False
    window = MainWindow(camera, config)
    window.show()
    sys.exit(app.exec_())
