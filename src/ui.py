import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QLineEdit, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from image_processor import convert_to_stl, get_contours, draw_line, largest_contour, process_size
from stl_utils import save_stl
from viewer import CustomGraphicsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image to STL Converter")
        self.setGeometry(100, 100, 800, 600)  # Initial size and position
        self.showMaximized()  # Maximize window on startup

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setColumnStretch(1, 4)  # Stretch the right column to take 80% of the window size

        # Create panel on the left side
        self.left_panel = QWidget()
        self.left_panel_layout = QVBoxLayout(self.left_panel)

        # Create buttons
        self.process_button = QPushButton("Process")        
        self.calculate_size_button = QPushButton("Calculate")
        self.makestl_button = QPushButton("Make STL")
        self.calculate_size_button.setEnabled(False)  # Initially disabled until height is entered

        # Add buttons to left panel
        self.left_panel_layout.addWidget(self.process_button)
        self.left_panel_layout.addWidget(self.calculate_size_button)
        self.left_panel_layout.addWidget(self.makestl_button)

        # Add left panel to the layout
        self.layout.addWidget(self.left_panel, 0, 0, 1, 1)  # Span one row and one column

        # Create QGraphicsView to display the image
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView(self.scene)
        self.layout.addWidget(self.view, 0, 1, 1, 4)  # Span one row and four columns

        # Create height input
        self.height_input_label = QLabel("Enter Height of red line (mm):")
        self.height_input = QLineEdit()

        height_input_layout = QHBoxLayout()
        height_input_layout.addWidget(self.height_input_label)
        height_input_layout.addWidget(self.height_input)

        self.left_panel_layout.addLayout(height_input_layout)
        # Connect button signals to slots
        self.process_button.clicked.connect(self.process_image)
        self.calculate_size_button.clicked.connect(self.process_size)
        self.height_input.textChanged.connect(self.enable_calculate_button)
        #self.makestl_button.clicked.connect(self.make_stl)

        # Initialize variables
        self.image_path = None
        self.image = None
        self.pixels_per_mm = None
        self.contours = None
        self.h = None
        self.w = None
        self.cropped = None

        # Initialize image item
        self.image_item = None

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
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if self.image_path:
            # Load image and display in QGraphicsView
            image = QPixmap(self.image_path)
            self.image_item = QGraphicsPixmapItem(image)
            self.scene.addItem(self.image_item)

    def process_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "Please open an image first.")
            return

        # Logic for processing image goes here
        import cv2
        import os

        assert os.path.exists(self.image_path)

        self.image = cv2.imread(self.image_path)
        self.contours = [largest_contour(get_contours(self.image)),]
        cv2.drawContours(self.image, self.contours, -1, (0, 255, 0), 3)
        self.h, self.w = draw_line(self.image, contours=self.contours)

        height, width, channel = self.image.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)

    def process_size(self):
        try:

            vertical_line_length_mm=float(self.height_input.text())
        except Exception:
            return
        
        self.cropped = process_size(self.image,
                                    total_height=self.h,
                                    vertical_line_length_mm=float(self.height_input.text()),
                                    vertical_line_length_px=self.h,
                                    total_width=self.w,
                                    contours=self.contours)

        height, width, channel = self.cropped.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.cropped.data, width, height, bytesPerLine, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)

    def enable_calculate_button(self):
        height = self.height_input.text()
        if height:
            self.calculate_size_button.setEnabled(True)
        else:
            self.calculate_size_button.setEnabled(False)

    
    def make_stl(self):
        # Example usage
        # Sample x, y coordinates
    
        vertical_line_length_mm=float(self.height_input.text())
        pixel_to_mm = 1
        
        save_stl(self.contours[0], pixel_to_mm)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
