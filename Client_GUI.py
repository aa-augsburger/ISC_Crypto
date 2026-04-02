import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtNetwork import QTcpSocket, QHostAddress
from MessageHandler import MessageHandler


class Client_GUI(QMainWindow):
    def __init__(self):

        #Gestion des classes crypto
        self.messageHandler = MessageHandler()

        #Creation de la fenetre
        super().__init__()
        ui_file = QFile("crypto_client.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        #Creation du QTCP Socket
        self.socket = QTcpSocket(self)
        self.ui.pb_connection.clicked.connect(self.connect_to_server)
        self.socket.connected.connect(self.connected_to_server)

        #Connection
        self.ui.pb_send.clicked.connect(self.send_message)
        self.ui.le_txtToSend.returnPressed.connect(self.send_message)
        self.socket.readyRead.connect(self.receive_message)

    def change_is_server(self):
        if self.ui.cb_is_server.isChecked():
            self.is_server = True
        else:
            self.is_server = False

    def show(self):
        self.ui.show()

    def connect_to_server(self):
        host = self.ui.le_host_address.text()
        port = int(self.ui.le_port_server.text())
        print(f"{host}{port}")
        self.socket.connectToHost(host, port)

    def connected_to_server(self):
        self.ui.lbl_server_status.setText("Connecté au serveur")
    def send_message(self):
        message = self.ui.le_txtToSend.text()
        print(message)
        ready_msg = self.messageHandler.create_text_message(message, self.ui.cb_is_server.isChecked(),self.ui.cb_is_intlist.isChecked())
        if message:
            self.socket.write(ready_msg)
    def receive_message(self):
        data = self.socket.readAll().data()
        msg = ""
        if data:
            print(f"Data: {data}")
            try:
                msg = self.messageHandler.parse_text_message(data)
                print(f"[FROM SERVER] {msg}")
            except Exception as e:
                print(f"Erreur dans le parsing - {e}")
        self.ui.te_reception.append(f"Reçu : {msg}")

