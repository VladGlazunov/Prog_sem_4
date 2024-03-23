import sys

from PyQt6.QtCore import QSize, Qt, QRectF
from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.image = QImage()
        self.userIsResizing = False
        self.resize(320, 240)

        self.setMouseTracking(True)
        self.positions = []

        self.setWindowTitle("My App")
        self.installEventFilter(self)


    def init_image(self, size: QSize):
        self.image = QImage(size.width(), size.height(), QImage.Format.Format_ARGB32)

    def paintEvent(self, e):
        width = self.image.width()
        height = self.image.height()
        for x in range(width):
            for y in range(height):
                Red = 255 - int(255 * x / width)
                Green = int(255 * x / width)
                Blue = int(255 * y / height)
                self.image.setPixel(x, y, QColor(Red, Green, Blue, 255).rgb())
        painter = QPainter(self)
        painter.drawImage(QRectF(0, 0, width, height), self.image)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()