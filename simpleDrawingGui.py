import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint


class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("💖 PyQt5 Image Drawer 💖")
        self.setGeometry(100, 100, 800, 600)

        # Apply pink theme
        self.setStyleSheet("background-color: #FFC0CB;")  # Light pink background

        # Button to open image with a stylish pink design
        self.button = QPushButton("🎀 Open Image 🎀", self)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #FF69B4;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #FF1493;
            }
        """)
        self.button.clicked.connect(self.load_image)

        # Label to display image with a pink border
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("border: 3px solid #FF69B4; border-radius: 10px;")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Variables for drawing
        self.image = None
        self.drawing = False
        self.erasing = False
        self.last_point = QPoint()

    def load_image(self):
        """Opens a file dialog and loads the selected image."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image = QPixmap(file_name)
            self.original_image = self.image.copy()  # Store a copy for clearing
            self.image_label.setPixmap(self.image)
            self.update()

    def is_inside_image(self, point):
        """Checks if a point is inside the displayed image area."""
        if self.image:
            img_rect = self.image_label.pixmap().rect()
            return img_rect.contains(point)
        return False

    def mousePressEvent(self, event):
        """Handles mouse press for drawing and erasing."""
        if self.image:
            img_pos = event.pos() - self.image_label.pos()
            if not self.is_inside_image(img_pos):
                return  # Prevent drawing outside the image

            if event.button() == Qt.LeftButton:
                self.drawing = True
                self.erasing = False
                self.last_point = img_pos
            elif event.button() == Qt.RightButton:
                self.erasing = True
                self.drawing = False
                self.last_point = img_pos

    def mouseMoveEvent(self, event):
        """Handles mouse movement for drawing and erasing."""
        if self.image and (self.drawing or self.erasing):
            img_pos = event.pos() - self.image_label.pos()
            if not self.is_inside_image(img_pos):
                return  # Prevent drawing outside the image

            painter = QPainter(self.image)
            if self.drawing:
                pen = QPen(Qt.red, 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            elif self.erasing:
                pen = QPen(Qt.white, 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

            painter.setPen(pen)
            painter.drawLine(self.last_point, img_pos)
            self.last_point = img_pos
            self.image_label.setPixmap(self.image)
            self.update()

    def mouseReleaseEvent(self, event):
        """Stops drawing or erasing when the mouse button is released."""
        if event.button() in [Qt.LeftButton, Qt.RightButton]:
            self.drawing = False
            self.erasing = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec_())
