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
        self.image[:, :, 0:3] = [0, 0, 10]  # Set RGB channels to red
        self.image[:, :, 3] = 100  # Set alpha channel (transparency)
        cv2.drawContours(self.image, contour, -1, (255, 0, 0), 2)

                # Define the text to be drawn
        text = "Drag and align to check"        # Choose the font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Choose the font scale and thickness
        font_scale = 1
        thickness = 1
        # Choose the text color in BGR
        color = (0, 255, 0)  # Green 
        # Choose the position to draw text
        position = (50, 50)  # Coordinates of the top-left corner of the text

        # Draw the text on the image
        cv2.putText(self.image, text, position, font, font_scale, color, thickness)

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
