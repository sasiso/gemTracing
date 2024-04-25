import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QFileDialog

from image_processor import get_contours
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image to STL Converter")
        self.setGeometry(100, 100, 800, 600)  # Initial size and position
        self.showMaximized()  # Maximize window on startup

        # Initialize central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QGraphicsView to display the image
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        # Create buttons
        self.process_button = QPushButton("Process")
        self.stl_button = QPushButton("Convert to STL")
        self.layout.addWidget(self.process_button)
        self.layout.addWidget(self.stl_button)

        # Connect button signals to slots
        self.process_button.clicked.connect(self.process_image)
        self.stl_button.clicked.connect(self.convert_to_stl)

        # Initialize variables
        self.image_path = None
        self.pixels_per_mm = None

        # Initialize image item
        self.image_item = None

        # Initialize calibration line
        self.calibration_line_start = None
        self.calibration_line_end = None

        # Initialize STL viewer
        self.stl_viewer = None

        # Create menu bar
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

    def open_image(self):
        # Open file dialog to select image file
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)")

        if self.image_path:
            # Load image and display in QGraphicsView
            image = QPixmap(self.image_path)
            self.image_item = QGraphicsPixmapItem(image)
            self.scene.addItem(self.image_item)

    def process_image(self):
        # Logic for processing image goes here
        # Load the image
        import cv2
        import os
        image_path = self.image_path
        assert os.path.exists(image_path)

        image = cv2.imread(image_path)
        contours = get_contours(image)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)

        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        self.image_item = QGraphicsPixmapItem(pixmap)

        self.scene.addItem(self.image_item )

    def convert_to_stl(self):
        # Logic for converting image to STL goes here
        pass

    def calibrate_pixels_to_mm(self):
        # Implement calibration feature
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
