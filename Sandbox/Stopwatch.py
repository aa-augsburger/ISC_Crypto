import sys
from PySide6 import *
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication


class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stopwatch")
        self.btn_stop = QPushButton("Stop")
        self.btn_reset = QPushButton("Reset")
        self.btn_start = QPushButton("Start")


        layout = QVBoxLayout()
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_reset)
        self.setLayout(layout)


        self.timer = QTimer()
        self.timer.setInterval(1000)


    def launch_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Stopwatch()
    window.show()
    sys.exit(app.exec_())