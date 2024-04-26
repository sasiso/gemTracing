from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setMouseTracking(True)
        self.zoom_factor = 1.1

    def wheelEvent(self, event):
        # Zoom Factor
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_factor
        else:
            zoom_factor = 1 / self.zoom_factor

        # Perform zoom
        self.scale(zoom_factor, zoom_factor)
