import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket

from Crypto.Shift import shift_int
from MessageHandler import MessageHandler
import re


class Client_GUI(QMainWindow):
    def __init__(self):

        #Gestion des classes crypto
        self.messageHandler = MessageHandler()

        #Variable globale
        self.task_awaited = "none" #flag pour savoir si on attend une tache du serveur
        self.nb_msg_task = 0
        self.buffer = []
        self.result_list = []

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
        #Shift
        self.ui.btn_ask_shift_encode.clicked.connect(lambda: self.ask_task(True, self.ui.sp_shift_encode_length.text()))
        self.ui.btn_ask_shift_decode.clicked.connect(lambda: self.ask_task(False ,self.ui.sp_shift_decode_length.text()))
        self.ui.btn_shift_encode.clicked.connect(self.shift_encode)
        self.ui.btn_shift_encode_check.clicked.connect(self.shift_encode_check)

        #connection au serveur au démarrage
        self.connect_to_server()

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

        if self.task_awaited != "none":
            self.buffer.append(msg)
        if len(self.buffer) == self.nb_msg_task:
            match self.task_awaited:
                case "shift":
                    self.shift_encode_parser()
                case "shift_encode_result":
                    self.shift_encode_result()
            self.task_awaited = "none"
            self.nb_msg_task = 0

    def write_log(self, origin, logs):
        self.ui.te_reception.append(f"{QTime.currentTime().toString('hh:mm:ss')} - [{origin}] : {logs}")

    def ask_task(self, is_encode, task_length = ""):
        mode = ""
        match self.ui.cipher_tab.currentIndex():
            case 1:
                mode = "shift"
                self.buffer_manager(mode, 2)
            case 2:
                mode = "vigenere"
        action = 'encode' if is_encode else 'decode'
        length = int(task_length) if task_length != '' else ''
        msg = f"task {mode} {action} {length}"
        print("demande de tache " + msg)
        self.send_message(False, msg, False, True)
        self.write_log("TACHE", msg)

    def buffer_manager(self, task, nb):
        self.nb_msg_task = nb
        self.task_awaited = task
        self.buffer.clear()


    ###############################################################################
    #
    #   SHIFT
    #
    ###############################################################################

    # ENCODE

    def shift_encode_parser(self):
        print("Fonction encode shift")
        key_text = self.buffer[0]
        match = re.search(r"\d+", key_text)
        key = match.group()
        text = self.buffer[1]
        self.ui.le_shift_encode_key.setText(key)
        self.ui.te_shift_encode_task.setText(text)
        print(f"clé{key}")
        print(f"text{text}")

    def shift_encode(self):
        print("Fonction shift encode")
        list_int = self.messageHandler.string_to_ints(self.ui.te_shift_encode_task.toPlainText())
        msg_encoded = shift_int(list_int, int(self.ui.le_shift_encode_key.text()))
        self.result_list = msg_encoded
        txt  = self.messageHandler.ints_to_string(msg_encoded)
        self.ui.te_shifted_task.setText(f"Message encodé : {txt}\nEn liste entier : {self.result_list}")

    def shift_encode_check(self):
        print("Fonction shift encode check")
        msg = self.messageHandler.string_to_ints(self.ui.te_shifted_task.toPlainText())
        self.buffer_manager("shift_result", 1)
        self.send_message(False, self.result_list, True)

    def shift_encode_result(self):
        if "correct" in self.buffer[0]:
            resultat = "L'encodage est correcte"
        else:
            resultat = "L'encodage est incorrecte"

        self.ui.lbl_shift_encode_result.setText(resultat)

    #DECODE

    ###############################################################################
    #
    #   VIGENERE
    #
    ###############################################################################

    def vgn_encode_parser(self):
        print("Fonction encode shift")
        key_text = self.buffer[0]
        match = re.search(r"\d+", key_text)
        key = match.group()
        text = self.buffer[1]
        self.ui.le_shift_encode_key.setText(key)
        self.ui.te_shift_encode_task.setText(text)
        print(f"clé{key}")
        print(f"text{text}")

    def vgn_encode(self):
        print("Fonction shift encode")
        list_int = self.messageHandler.string_to_ints(self.ui.te_shift_encode_task.toPlainText())
        msg_encoded = shift_int(list_int, int(self.ui.le_shift_encode_key.text()))
        self.result_list = msg_encoded
        txt  = self.messageHandler.ints_to_string(msg_encoded)
        self.ui.te_shifted_task.setText(f"Message encodé : {txt}\nEn liste entier : {self.result_list}")

    def vgn_encode_check(self):
        print("Fonction shift encode check")
        msg = self.messageHandler.string_to_ints(self.ui.te_shifted_task.toPlainText())
        self.buffer_manager("shift_encode_result", 1)
        self.send_message(False, self.result_list, True)

    def vgn_encode_result(self):
        if "correct" in self.buffer[0]:
            resultat = "L'encodage est correcte"
        else:
            resultat = "L'encodage est incorrecte"

        self.ui.lbl_shift_encode_result.setText(resultat)
