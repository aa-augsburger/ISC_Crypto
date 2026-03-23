import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtNetwork import QTcpSocket


class Client_GUI(QMainWindow):
    def __init__(self):

        #Creation de la fenetre
        super().__init__()
        ui_file = QFile("crypto_client.ui")
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        self.ui.show()
        ui_file.close()
        self.setCentralWidget(self.ui)

        #Creation du QTCP Socket

