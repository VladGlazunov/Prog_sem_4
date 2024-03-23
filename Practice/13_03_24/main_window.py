from math import floor, log10

from PyQt6.QtCore import QSize, Qt, QPoint, QPointF, QRectF, QObject, pyqtSignal, QTimer
from PyQt6.QtGui import QImage, QResizeEvent, QPaintEvent, QPainter, QMatrix4x4, QTransform, QPen, QMouseEvent, \
    QWheelEvent, QStaticText, QColor, QBrush
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


app = QApplication([])

window = QMainWindow
window.show()

app.exec()
