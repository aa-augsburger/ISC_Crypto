import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket
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
        self.socket.connected.connect(self.connected_to_server)
        self.socket.stateChanged.connect(self.network_changed)
        self.ui.pb_connection.clicked.connect(self.connect_to_server)
        self.ui.pb_test.clicked.connect(self.test_connection)

        #Connection
        self.ui.pb_send.clicked.connect(self.send_message)
        self.ui.le_txtToSend.returnPressed.connect(self.send_message)
        self.socket.readyRead.connect(self.receive_message)

    def show(self):
        self.ui.show()

    def network_changed(self, state):
        if state == QAbstractSocket.SocketState.UnconnectedState:
            curr_state = 'Déconnexion'
        elif state == QAbstractSocket.SocketState.HostLookupState:
            curr_state = 'Host Lookup'
        elif state == QAbstractSocket.SocketState.ConnectingState:
            curr_state = 'Connexion en cours'
        elif state == QAbstractSocket.SocketState.ConnectedState:
            curr_state = 'Connecté'
        elif state == QAbstractSocket.SocketState.BoundState:
            curr_state = 'Bound'
        elif state == QAbstractSocket.SocketState.ClosingState:
            curr_state = 'Fermeture en cours'
        self.ui.lbl_server_status.setText(f"{curr_state} à {QTime.currentTime().toString('hh:mm:ss')} ")

    def test_connection(self):
        pass
    def connect_to_server(self):
        host = self.ui.le_host_address.text()
        port = int(self.ui.le_port_server.text())
        print(f"{host}{port}")
        self.socket.connectToHost(host, port)


    def connected_to_server(self):
        self.ui.lbl_server_status.setText(f"Connecté au serveur à {QTime.currentTime().toString('hh:mm:ss')} ")
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

