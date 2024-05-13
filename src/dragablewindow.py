import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import Qt, QPoint
import cv2
class DraggableWidget(QWidget):
    def __init__(self, parent, width, height, contour):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.setGeometry(50, 50, self.height, self.width)  
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.dragging = False
        self.offset = QPoint(0, 0)

        # Create an empty image with transparent red color
        self.image = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self.image[:, :, 0:3] = [0, 0, 255]  # Set RGB channels to red
        self.image[:, :, 3] = 100  # Set alpha channel (transparency)
        cv2.drawContours(self.image, contour, -1, (255, 0, 0), 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, QImage(self.image, self.image.shape[1], self.image.shape[0], QImage.Format_RGBA8888))

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.offset = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
