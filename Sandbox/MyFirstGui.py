import sys
from PySide6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISC Crypto")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.myLayout = QVBoxLayout(self.centralWidget)

        self.myLabel = QLabel("Whats must be on a pizza ? ")
        self.myLayout.addWidget(self.myLabel)

        self.myInput = QLineEdit("You know the answer")
        self.myLayout.addWidget(self.myInput)

        self.myButton = QPushButton("Encrypt")
        self.myLayout.addWidget(self.myButton)

        self.setFixedSize(300, 200)

        self.myButton.clicked.connect(self.showItem)


    def showItem(self):
        QMessageBox.information(self, "Message Encrypted", "Message Encrypted")

app = QApplication(sys.argv)
windows = MainWindow()
windows.show()
sys.exit(app.exec())