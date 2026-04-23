import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket

from Crypto.RSA import encrypt_RSA, generate_keypair
from Crypto.Shift import shift_int
from Crypto.Vigenere import int_vigenere_encrypt
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
        self.public_key = ""
        self.rsa_key = ()

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
        self.ui.btn_vgn_ask_encode.clicked.connect(lambda: self.ask_task(True, self.ui.sp_vgn_length.text()))
        self.ui.btn_vgn_encode.clicked.connect(self.vgn_encode)
        self.ui.btn_vgn_check.clicked.connect(self.vgn_encode_check)
        self.ui.btn_rsa_ask_encode.clicked.connect(lambda: self.ask_task(True, self.ui.sp_rsa_length.text()))
        self.ui.btn_rsa_encode.clicked.connect(self.rsa_encode)
        self.ui.btn_rsa_check_encode.clicked.connect(self.rsa_encode_check)
       # self.ui..clicked.connect(self.)
        self.ui.btn_generate_rsa.clicked.connect(self.rsa_generate_key)
        self.ui.btn_rsa_send_key.clicked.connect(self.send_rsa_key)
        self.ui.btn_rsa_decode.clicked.connect(self.rsa_decode)
        self.ui.btn_rsa_decoded_check.clicked.connect(self.rsa_decode_check)




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
                case "vigenere":
                    self.vgn_encode_parser()
                case "vgn_encode_result":
                    self.vgn_encode_result()
                case "RSA":
                    self.rsa_encode_parser()
                case "rsa_encode_result":
                    self.rsa_encode_result()
                case "rsa_rcv_encoded":
                    self.rsa_rcv_encoded()
                case "rsa_decode_result":
                    self.rsa_decode_result()

            self.task_awaited = "none"
            self.nb_msg_task = 0

    def write_log(self, origin, logs):
        self.ui.te_reception.append(f"{QTime.currentTime().toString('hh:mm:ss')} - [{origin}] : {logs}")

    def ask_task(self, is_encode, task_length = ""):
        mode = ""
        match self.ui.cipher_tab.currentIndex():
            case 0:
                mode = "shift"
                self.buffer_manager(mode, 2)
            case 1:
                mode = "vigenere"
                self.buffer_manager(mode, 2)
            case 2:
                mode = "RSA"
                self.buffer_manager(mode, 2)

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

    def resultat(self, text):
        if "correct" in text:
            resultat = "L'encodage est correcte"
        elif "invalid" in text:
            resultat = "L'encodage est incorrecte"
        else:
            resultat = "Pas de tâche en cours"
        return resultat


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
        self.buffer_manager("shift_encode_result", 1)
        self.send_message(False, self.result_list, True)

    def shift_encode_result(self):
        self.ui.lbl_shift_encode_result.setText(self.resultat(self.buffer[0]))

    #DECODE

    def shift_decode_parser(self):
        print("Fonction decode shift")
        key_text = self.buffer[0]
        match = re.search(r"\d+", key_text)
        key = match.group()
        text = self.buffer[1]
        self.ui.le_shift_decode_key.setText(key)
        self.ui.te_shift_decode_task.setText(text)
        print(f"clé{key}")
        print(f"text{text}")

    def shift_decode(self):
        print("Fonction shift decode")
        list_int = self.messageHandler.string_to_ints(self.ui.te_shift_decode_task.toPlainText())
        msg_decoded = shift_int(list_int, int(self.ui.le_shift_decode_key.text()))
        self.result_list = msg_decoded
        txt  = self.messageHandler.ints_to_string(msg_decoded)
        self.ui.te_shifted_task.setText(f"Message encodé : {txt}\n\nEn liste entier : {self.result_list}")

    def shift_decode_check(self):
        print("Fonction shift decode check")
        msg = self.messageHandler.string_to_ints(self.ui.te_shifted_task.toPlainText())
        self.buffer_manager("shift_decode_result", 1)
        self.send_message(False, self.result_list, True)

    def shift_decode_result(self):
        self.ui.lbl_shift_decode_result.setText(self.resultat(self.buffer[0]))

    ###############################################################################
    #
    #   VIGENERE
    #
    ###############################################################################

    def vgn_encode_parser(self):
        print("Fonction encode vigenere")
        key_text = self.buffer[0]
        match = re.search(r"\S+$", key_text)
        key = match.group()
        text = self.buffer[1]
        self.ui.txt_vgn_encode_key.setText(key)
        self.ui.txt_vgn_encode_task.setText(text)
        print(f"clé{key}")
        print(f"text{text}")

    def vgn_encode(self):
        print("Fonction shift encode")
        int_task = self.messageHandler.string_to_ints(self.ui.txt_vgn_encode_task.toPlainText())
        int_key = self.messageHandler.string_to_ints(self.ui.txt_vgn_encode_key.text())
        msg_encoded = int_vigenere_encrypt(int_task, int_key)
        self.result_list = msg_encoded
        txt  = self.messageHandler.ints_to_string(msg_encoded)
        self.ui.txt_vgn_encoded.setText(f"Message encodé : {txt}\n\nEn liste entier : {self.result_list}")

    def vgn_encode_check(self):
        print("Fonction vgn encode check")
        msg = self.messageHandler.string_to_ints(self.ui.te_shifted_task.toPlainText())
        self.buffer_manager("vgn_encode_result", 1)
        self.send_message(False, self.result_list, True)

    def vgn_encode_result(self):
        self.ui.txt_vgn_encode_result.setText(self.resultat(self.buffer[0]))

    ###############################################################################
    #
    #   RSA
    #
    ###############################################################################

    def rsa_encode_parser(self):
        print("Fonction encode RSA")
        key_text = self.buffer[0]
        match = re.search(r"n=(\d+),\s*e=(\d+)", key_text)
        modulus = int(match.group(1))
        exponent = int(match.group(2))
        text = self.buffer[1]
        self.ui.txt_rsa_en_mod.setText(str(modulus))
        self.ui.txt_rsa_en_exp.setText(str(exponent))
        self.ui.txt_rsa_encode_task.setText(text)
        print(f"text{text}")

    def rsa_encode(self):
        print("Fonction rsa encode")
        int_task = self.messageHandler.string_to_ints(self.ui.txt_rsa_encode_task.toPlainText())
        mod = int(self.ui.txt_rsa_en_mod.text())
        exp = int(self.ui.txt_rsa_en_exp.text())
        msg_encoded = encrypt_RSA(int_task, (mod, exp))
        self.result_list = msg_encoded
        txt  = self.messageHandler.ints_to_string(msg_encoded)
        self.ui.txt_rsa_encoded.setText(f"Message encodé : {txt}\n\nEn liste entier : {self.result_list}")

    def rsa_encode_check(self):
        print("Fonction RSA encode check")
        msg = self.messageHandler.string_to_ints(self.ui.te_shifted_task.toPlainText())
        self.buffer_manager("rsa_encode_result", 1)
        self.send_message(False, self.result_list, True)

    def rsa_encode_result(self):
        self.ui.txt_rsa_encode_result.setText(self.resultat(self.buffer[0]))

# RSA DECODE

    def rsa_generate_key(self):
        self.ask_task(False, self.ui.rsa_decode_length.text())
        print("Fonction RSA generate key")
        keypair = generate_keypair()
        public_key, private_key = keypair
        self.rsa_key = private_key
        self.public_key = public_key
        self.ui.txt_rsa_key.setText(f"Clé privée : {public_key}, Clé publique : {private_key}")

    def send_rsa_key(self):
        n, e = self.public_key
        key = f"{n}, {e}"
        print(f"RSA PUBLIC KEY {key}")
        self.send_message(False, key, False)
        self.buffer_manager("rsa_rcv_encoded", 1)

    def rsa_rcv_encoded(self):
        self.ui.txt_rsa_rcv.setText(self.buffer[0])

    def rsa_decode(self):
        print("Fonction rsa decode")
        text = self.ui.txt_rsa_rcv.toPlainText()
        int_list = list(map(int, text.split()))
        msg_encoded = encrypt_RSA(int_list, self.rsa_key)
        self.result_list = msg_encoded
        txt  = self.messageHandler.ints_to_string(msg_encoded)
        self.ui.txt_rsa_decoded.setText(f"Message décodé : {txt}\n\nEn liste entier : {self.result_list}")

    def rsa_decode_check(self):
        print("Fonction rsa decode check")
        msg = self.messageHandler.string_to_ints(self.ui.te_shifted_task.toPlainText())
        self.buffer_manager("rsa_decode_result", 1)
        self.send_message(False, self.result_list, True)

    def rsa_decode_result(self):
        self.ui.lbl_decoded_resultat_rsa.setText(self.resultat(self.buffer[0]))


