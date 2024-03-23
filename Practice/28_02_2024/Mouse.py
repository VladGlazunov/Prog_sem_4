import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QLabel, QTextEdit


class MainWindow(QMainWindow):
    button = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMouseTracking(True)
        self.setWindowTitle("My App")
        self.label = QLabel("Click in this window")
        self.resize(QSize(400, 300))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, e):
        self.label.setText(f"mousePosision: x{e.pos().x()}, y{e.pos().y()}")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseDoubleClickEvent LEFT")

        if e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseDoubleClickEvent MIDDLE")

        if e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseDoubleClickEvent RIGHT")

    def keyPressEvent(self, e):
        self.label.setText(f"keyPress:{e.key()}")

    def keyReleaseEvent(self, e):
        keycode = e.key()
        if 0 <= keycode <= 255:
            self.label.setText(f"keyRelease:{chr(keycode)}")
        else:
            self.label.setText(f"keyRelease:{e.key()}")
    #дореализовать вывод несколькизх данных одновременно (одной или несколькими строками)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
