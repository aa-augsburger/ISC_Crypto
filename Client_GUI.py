import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket

from Crypto_Algo.DiffieHellman import generate_prime_number, find_generator, generate_private_key, generate_public_key, \
    compute_shared_key
from Crypto_Algo.Hashing import hashing
from Crypto_Algo.RSA import encrypt_RSA, generate_keypair
from Crypto_Algo.Shift import shift_int, frequential_analysis, unshift_int
from Crypto_Algo.Vigenere import int_vigenere_encrypt
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
        self.hashed = ""

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
        self.ui.btn_toggle_connection.clicked.connect(self.toggle_connection)
        self.socket.readyRead.connect(self.receive_message)

        #Connection
        self.ui.pb_send.clicked.connect(lambda: self.send_message())
        self.ui.le_txtToSend.returnPressed.connect(self.send_message)
        #Shift
        self.ui.btn_ask_shift_encode.clicked.connect(lambda: self.ask_task(True, self.ui.sp_shift_encode_length.text()))
        self.ui.btn_ask_shift_decode.clicked.connect(lambda: self.ask_task(False ,self.ui.sp_shift_decode_length.text()))
        self.ui.btn_shift_encode.clicked.connect(self.shift_encode)
        self.ui.btn_shift_encode_check.clicked.connect(self.shift_encode_check)
        self.ui.btn_shift_decode.clicked.connect(self.shift_decode)
        self.ui.btn_shift_decode_verify.clicked.connect(self.shift_decode_check)
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
        self.ui.btn_ask_hash.clicked.connect(lambda: self.ask_task(True))
        self.ui.btn_hash.clicked.connect(self.hash)
        self.ui.btn_hash_check.clicked.connect(self.hash_check)
        self.ui.btn_ask_hash_verify.clicked.connect(lambda: self.ask_task(False))
        self.ui.btn_hash_verify.clicked.connect(self.hash_verify)
        self.ui.btn_dh_mod.clicked.connect(self.generate_modulus)
        self.ui.btn_dh_send.clicked.connect(self.send_modulus)
        self.ui.btn_dh_key.clicked.connect(self.generate_key)
        self.ui.btn_dh_secret.clicked.connect(self.generate_secret)
        self.ui.btn_dh_verify.clicked.connect(self.check_secret)


        #connection au serveur au démarrage
        self.connect_to_server()

    def show(self):
        self.ui.show()

    def network_changed(self, state):
        curr_state = state
        match  state :
            case QAbstractSocket.SocketState.UnconnectedState:
                curr_state = 'Déconnecté'
                self.ui.btn_toggle_connection.setText("Se connecter")
            case QAbstractSocket.SocketState.HostLookupState:
                curr_state = 'Recherche d hôte'
            case QAbstractSocket.SocketState.ConnectingState:
                curr_state = 'Connexion en cours...'
            case QAbstractSocket.SocketState.ConnectedState:
                curr_state = 'Connecté'
                self.ui.btn_toggle_connection.setText("Se déconnecter")
            case QAbstractSocket.SocketState.BoundState:
                curr_state = 'Etat lié'
            case QAbstractSocket.SocketState.ClosingState:
                curr_state = 'Déconnexion en cours...'
        log = f"{curr_state} "
        self.write_log("RESEAU", log)
        self.ui.lbl_server_status.setText(f"{QTime.currentTime().toString('hh:mm:ss')} - {log}")

    def toggle_connection(self):
        if self.socket.state() == QAbstractSocket.SocketState.ConnectedState:
            self.disconnect_from_server()
        else:
            self.connect_to_server()


    def connect_to_server(self):
        host = self.ui.le_host_address.text()
        port = int(self.ui.port_server.text())
        print(f"{host}{port}")
        self.socket.connectToHost(host, port)

    def disconnect_from_server(self):
        self.socket.disconnectFromHost()



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

        print(self.task_awaited)
        if self.task_awaited != "none":
            print("ajout de message dans le buffer")
            self.buffer.append(msg)
            print(len(self.buffer))
        if len(self.buffer) == self.nb_msg_task:
            match self.task_awaited:
                case "shift encode":
                    self.shift_encode_parser()
                case "shift decode":
                    self.shift_decode_parser()
                case "shift_encode_result":
                    self.shift_encode_result()
                case "shift_decode_result":
                    self.shift_decode_result()
                case "vigenere encode":
                    self.vgn_encode_parser()
                case "vgn_encode_result":
                    self.vgn_encode_result()
                case "RSA encode":
                    self.rsa_encode_parser()
                case "rsa_encode_result":
                    self.rsa_encode_result()
                case "rsa_rcv_encoded":
                    self.rsa_rcv_encoded()
                case "rsa_decode_result":
                    self.rsa_decode_result()
                case "hash hash":
                    self.hash_parser()
                case "hash_result":
                    self.hash_result()
                case "hash verify":
                    self.hash_verify_parser()
                case "hash_verify_result":
                    self.hash_verify_result()
                case "DifHel":
                    self.rcv_key_1()
                case "rcv_key_2":
                    print("rcv key 2")
                    self.rcv_key_2()
                case "dh check key":
                    self.dh_result()

    def write_log(self, origin, logs):
        self.ui.te_reception.append(f"{QTime.currentTime().toString('hh:mm:ss')} - [{origin}] : {logs}")

    def ask_task(self, is_encode, task_length = ""):
        mode = ""
        action = ""
        match self.ui.cipher_tab.currentIndex():
            case 0:
                mode = "shift encode" if is_encode else "shift decode"
                self.buffer_manager(mode, 2)
            case 1:
                mode = "vigenere encode"
                self.buffer_manager(mode, 2)
            case 2:
                mode = "RSA encode" if is_encode else "RSA decode"
                self.buffer_manager(mode, 2)
            case 3:
                mode = "DifHel"
                self.buffer_manager(mode, 2)
            case 4:
                mode = 'hash hash' if is_encode else 'hash verify'
                self.buffer_manager(mode, 2)
        length = int(task_length) if task_length != '' else ''
        msg = f"task {mode} {action} {length}"
        print("demande de tache " + mode + " - msg: " + msg)
        self.send_message(False, msg, False, True)
        self.write_log("TACHE", msg)

    def buffer_manager(self, task, nb, clear = True):
        self.nb_msg_task = nb
        self.task_awaited = task
        if clear:
            self.buffer.clear()

    def resultat(self, text):
        txt_result = ""
        if "correct"  in text.lower():
            txt_result = "L'encodage est correcte"
        elif "invalid" in text.lower() or "not" in text.lower():
            txt_result = "L'encodage est incorrecte"
        elif text == "The hash corresponds to the sent message":
            txt_result = "Le hash est correcte"
        elif text == "The hash does not correspond to the message":
            txt_result = "Le hash n'est pas correcte"
        elif text == "The shared secret has been validated !":
            txt_result = "Le secret commun a été validé"
        elif text == "The shared secret is not the same as the server, try again":
            txt_result = "Le secret commun N'a PAS été validé !"
        else:
            txt_result = "Pas de tâche en cours"
        return txt_result


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
        text = self.buffer[1]
        self.ui.txt_shift_decode_task.setText(text)


    def shift_decode(self):
        print("Fonction shift decode")
        list_int = self.messageHandler.string_to_ints(self.ui.txt_shift_decode_task.toPlainText())
        guess_key = frequential_analysis(list_int)
        print("Guess key : ", guess_key)
        msg_decoded = unshift_int(list_int, guess_key)
        self.result_list = msg_decoded
        txt  = self.messageHandler.ints_to_string(msg_decoded)
        self.ui.guessed_shift.setValue(guess_key)
        self.ui.txt_shift_decode_log.setText(f"Message décodé : {txt}\n\nEn liste entier : {self.result_list}")

    def shift_decode_check(self):
        print("Fonction shift decode check")
        key = str(self.ui.guessed_shift.value())
        self.buffer_manager("shift_decode_result", 1)
        self.send_message(False, key, False)

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
        self.ui.txt_rsa_key.setText(f"Clé publique : {public_key}, Clé privée : {private_key}")

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

        ###############################################################################
        #
        #   HASH
        #
        ###############################################################################

    #HASH HASH

    def hash_parser(self):
        print("Fonction hash parser")
        text = self.buffer[1]
        self.ui.txt_hash_task.setPlainText(text)

    def hash(self):
        print("Fonction hash")
        text = self.ui.txt_hash_task.toPlainText()
        msg_encoded = hashing(text)
        self.ui.txt_hashed.setText(f"{msg_encoded}")

    def hash_check(self):
        print("Fonction hash check")
        hashed =  self.ui.txt_hashed.toPlainText()
        self.buffer_manager("hash_result", 1)
        self.send_message(False, hashed, False)

    def hash_result(self):
        self.ui.lbl_hash_result.setText(self.resultat(self.buffer[0]))

        # HASH VERIFY

    def hash_verify_parser(self):
        print("Fonction hash_verify parser")
        rcv_msg = self.buffer[1].split("CSI")
        rcv_text = rcv_msg[0]
        rcv_hash = rcv_msg[1].replace('\x00', '').replace('@', '')

        self.ui.txt_hash_verify_text.setText(rcv_text)
        self.ui.txt_hash_verify_hash.setText(rcv_hash)



    def hash_verify(self):
        print("Fonction hash_verify")
        text = self.ui.txt_hash_verify_text.text()
        msg_encoded = hashing(text)
        self.ui.txt_hash_verifyed.setText(f"{msg_encoded}")

    def hash_verify_check(self):
        print("Fonction hash_verify check")
        ourHash = self.ui.txt_hash_verifyed.text()
        serverHash = self.ui.txt_hash_verify_hash.text()
        self.buffer_manager("hash_verify_result", 1)
        result = "true" if ourHash == serverHash else "false"
        self.send_message(False, result, False)

    def hash_verify_result(self):
        self.ui.lbl_hash_verify_result.setText(self.resultat(self.buffer[0]))


        ###############################################################################
        #
        #   DIFFIE HELLEMAN
        #
        ###############################################################################

    def generate_modulus(self):
        print("Fonction generate_modulus")
        max = self.ui.max_modulo.value()
        prime = generate_prime_number(max)
        generator = find_generator(prime)
        self.ui.mod_world.setValue(prime)
        self.ui.generator.setValue(generator)

    def send_modulus(self):
        print("Fonction send_modulus")
        mod = f"{self.ui.mod_world.value()}, {self.ui.generator.value()}"
        self.ask_task(False)
        self.send_message(False, mod, False)

    #permet la gestion si le serveur envoie la clé en 1 message ou en séparer
    def rcv_key_1(self):
        print("Fonction rcv_key 1")
        print(self.buffer[1])
        if "CSI" in self.buffer[1]:
            print("parsing csi")
            rcv_msg = self.buffer[1].split("CSI")
            rcv_key = rcv_msg[1].replace('\x00', '')
            cleaned_key = ""
            for c in rcv_key:
                if c.isdigit():
                    cleaned_key += c

            print(cleaned_key)
            self.ui.pub_gb.setValue(int(cleaned_key))
        else:
            print("on attend la clé séparement")
            self.buffer_manager("rcv_key_2", 3, False)


    def rcv_key_2(self):
        print("Fonction rcv_key 2")
        self.ui.pub_gb.setValue(int(self.buffer[2]))

    def generate_key(self):
        print("Fonction generate_key")
        mod_world = self.ui.mod_world.value()
        generator = self.ui.generator.value()
        private_a = generate_private_key(mod_world)
        self.ui.priv_a.setValue(private_a)

        public_ga = generate_public_key(generator, private_a, mod_world)
        self.ui.pub_ga.setValue(public_ga)
        self.send_message(False, str(public_ga), False)

    def generate_secret(self):
        print("Fonction generate_secret")
        public_key = self.ui.pub_gb.value()
        secret_key = self.ui.priv_a.value()
        mod = self.ui.mod_world.value()
        mutual_secret = compute_shared_key(public_key, secret_key, mod)
        self.ui.mut_secret.setValue(mutual_secret)


    def check_secret(self):
        print("Fonction check_key")
        result = str(self.ui.mut_secret.value())
        self.buffer_manager("dh check key", 1)
        self.send_message(False, result, False)

    def dh_result(self):
        print("Fonction dh_result")
        self.ui.txt_difi_result.setText(self.resultat(self.buffer[0]))
