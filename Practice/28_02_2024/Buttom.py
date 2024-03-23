import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QLabel


class MainWindow(QMainWindow):
    button = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.resize(QSize(400, 300))
        self.button.clicked.connect(self.button_clicked)

        self.setCentralWidget(self.button)

    def button_clicked(self, checked):
        self.setWindowTitle("Clicked!")
        self.button.setText("Checked" if checked else "Not checked")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
