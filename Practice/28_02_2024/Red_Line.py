import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QLabel, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.resize(QSize(400, 300))

    def paintEvent(self, e):

        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.red, 3)
        painter.setPen(pen)
        painter.drawLine(100, int(self.rect().height() / 2), self.rect().width() - 100, int(self.rect().height() / 2))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()