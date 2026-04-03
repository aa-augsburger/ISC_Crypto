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
        self.socket.stateChanged.connect(self.network_changed)
        self.ui.pb_connection.clicked.connect(self.connect_to_server)
        self.ui.pb_test.clicked.connect(self.test_connection)
        self.socket.readyRead.connect(self.receive_message)

        #Connection
        self.ui.pb_send.clicked.connect(lambda: self.send_message())
        self.ui.le_txtToSend.returnPressed.connect(self.send_message)
        self.ui.pb_ask_encode.clicked.connect(lambda: self.ask_task(True))
        self.ui.pb_ask_decode.clicked.connect(lambda: self.ask_task(False))

    def show(self):
        self.ui.show()

    def network_changed(self, state):
        curr_state = state
        match  state :
            case QAbstractSocket.SocketState.UnconnectedState:
                curr_state = 'Déconnecté'
            case QAbstractSocket.SocketState.HostLookupState:
                curr_state = 'Recherche d hôte'
            case QAbstractSocket.SocketState.ConnectingState:
                curr_state = 'Connexion en cours...'
            case QAbstractSocket.SocketState.ConnectedState:
                curr_state = 'Connecté'
            case QAbstractSocket.SocketState.BoundState:
                curr_state = 'Etat lié'
            case QAbstractSocket.SocketState.ClosingState:
                curr_state = 'Déconnexion en cours...'
        log = f"{curr_state} "
        self.write_log("RESEAU", log)
        self.ui.lbl_server_status.setText(f"{QTime.currentTime().toString('hh:mm:ss')} - {log}")

    def test_connection(self):
        pass
    def connect_to_server(self):
        host = self.ui.le_host_address.text()
        port = int(self.ui.le_port_server.text())
        print(f"{host}{port}")
        self.socket.connectToHost(host, port)

    def send_message(self, from_user = True, input = "", is_intlist = False, is_server = True):
        ready_msg = ""
        msg = ""
        print("on préparer le message")
        if from_user:
            msg = self.ui.le_txtToSend.text()
            ready_msg = self.messageHandler.create_text_message(msg, self.ui.cb_is_server.isChecked(),self.ui.cb_is_intlist.isChecked())
        else:
            ready_msg = self.messageHandler.create_text_message(input, is_server, is_intlist)
        if ready_msg:
            self.socket.write(ready_msg)
            print("Message envoye : " + msg)
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
        self.write_log("SERVEUR", msg)

    def write_log(self, origin, logs):
        self.ui.te_reception.append(f"{QTime.currentTime().toString('hh:mm:ss')} - [{origin}] : {logs}")

    def ask_task(self, is_encode):
        mode = ""
        length = int(self.ui.sp_length_task.text())

        match self.ui.cipher_tab.currentIndex():
            case 0:
                mode = "shift"
            case 1:
                mode = "vigenere"
        msg = f"task {mode} {"encode" if is_encode else "decode"} {length}"
        print("demande de tache " + msg)
        self.send_message(False, msg, False, True)
        self.write_log("TACHE", msg)


def send_result(self, result):
    self.send_message(False, result, True)
