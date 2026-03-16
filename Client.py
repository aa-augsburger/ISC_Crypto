import msvcrt
import sys

from MessageHandler import MessageHandler
from NetworkManager import NetworkManager
from Crypto.Shift import *
from Crypto.Vigenere import *

class Client:

    def __init__(self, address, port):
        self.debug_mode =  False
        self.networkManager = NetworkManager(address, port)
        self.messageHandler = MessageHandler(self.networkManager)
        self.buffer = []
        self.message_list = []
        self.debug(True)


    def command_controller(self):
        input = self.getInput()
        self.message_list.append(f"Commande : {input}")
        parsing_return = self.parseInput(input)
        msg_awaited = parsing_return[0]
        change_buffer = parsing_return[1]
        if change_buffer:
            self.buffer = self.messageHandler.add_data(msg_awaited)
            self.messageHandler.get_messages(self.buffer)
            for msg in self.buffer:
                self.message_list.append(f"Serveur : {msg}")

    def getInput(self):
        inp = input("Entrer votre commande : ")
        return inp

    def parseInput(self, input):
        inputTab = input.split(" ")
        msg_awaited = 0
        change_buffer = False

        if(inputTab[0][0] != "/"):
            self.send_command(input)
            msg_awaited = 2
            change_buffer = True
        if(inputTab[0][0].isdigit()):
            self.send_command(inputTab[0])
            msg_awaited = 1

        else:
            match len(inputTab):
                case 1:
                    match inputTab[0]:
                        case "/help":
                            self.help()
                        case "/health":
                            self.health()
                            msg_awaited = 0
                        case "/exit"  | "/quit" | "/q":
                            self.quit()
                        case "/clear":
                            self.clear()

                        case "/show":
                            self.show()
                        case "/list":
                            self.list(10)
                        case "/listen" | "/eavedrop":
                            self.eavedrop()
                case 2:
                    match inputTab[0]:
                        case "/debug":
                            if(inputTab[1] == "on" or inputTab[1] == "true"):
                                self.debug(True)
                            else:
                                self.debug(False)
                        case "/list":
                            self.list(inputTab[1])
                        case "/decode":
                            match inputTab[1]:
                                case "shift":
                                    print("Tentative de décodage")
                                    if len(self.buffer) == 1: self.decode_shift(self.buffer[1])
                                    else: print("Pas de message à décoder")
                                    msg_awaited = 0
                                    change_buffer = True
                                case "vigenere":
                                    self.decode_vigenere(self.buffer[0], inputTab[2])
                                    msg_awaited = 1
                                    change_buffer = True


                case 3:
                    match inputTab[0]:
                        case "/encode":
                            match inputTab[1]:
                                case "shift":
                                    self.encode_shift(self.buffer[1], inputTab[2])
                                    change_buffer = True
                                    msg_awaited = 1
                                case "vigenere":
                                    self.encode_vigenere(self.buffer[1], inputTab[2])
                                    change_buffer = True
                                    msg_awaited = 1

        if self.debug_mode: print(f"Message attendu-s : {msg_awaited}")
        return msg_awaited, change_buffer

    def help(self):
        with open("help.txt", "r") as file:
            help_lines = file.read().split("/n")

        for line in help_lines:
            print(line)

    def eavedrop(self):
        print("===== MODE ECOUTE =====")
        try:
            while True:
                data = self.networkManager.receive()
                if data:
                    msg = self.messageHandler.parse_text_message(data)
                    print(f"[EAVESDROP] {msg}")
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode().lower()
                    if key == 'q':
                        print("\n===== FIN DU MODE ECOUTE =====")
                        break
        except Exception as e:
            print(f"[ERREUR] {e}")




    def health(self):
        try:
            self.send_command("/health")
        except Exception as e:
            print(f"Erreur de connexion - {e}")
            return

        if(len(self.messageHandler.add_data(1)) != 0):
            print("Connecté au serveur")
        else:
            print("Connecté au serveur, mais de message de retour")

    def quit(self):
        self.networkManager.close()
        print("Au plaisir d'avoir pu chiffrer avec vous ! Au revoir")
        sys.exit(0)

    def clear(self):
        pass
    def clear_buffer(self, clear_plain):
        self.buffer.clear()
        print("Le buffer a été supprimé")

    def show(self):
        print("=============== CONTENT OF THE BUFFER ==============")
        for msg in self.buffer:
            print(msg)
        print("=============== END BUFFER ==============")
    def list(self, n):
        print("=============== LISTE DES MESSAGES ==============")
        for msg in self.message_list:
            print(msg)
        print("=============== FIN DES MESSAGES ==============")

    def debug(self, enable):
        if enable:
            self.debug_mode = True
            self.networkManager.debug_mode = True
            self.messageHandler.debug_mode = True
            print("Debug mode on")
        else:
            self.debug_mode = False
            self.messageHandler.debug_mode = False
            self.networkManager.debug_mode = False
            print("Debug mode off")

    def send_command(self, msg):
        self.message_list.append(f"Client : {msg}")
        self.send_msg(msg)
    def encode_shift(self, msg, shift_value):
        #msg_encoded = shift(msg, int(shift_value))
        list_int = self.messageHandler.string_to_ints(msg)
        msg_encoded = shift_int(list_int, shift_value)
        if self.debug_mode: print(f"Encryption : {msg_encoded}")
        self.send_msg(msg_encoded, True, True)
    def decode_shift(self,encoded_msg):
        encoded_int = self.messageHandler.string_to_ints(encoded_msg)
        if self.debug_mode: print(f"Encoded Int : {encoded_int}")
        unshifted_int = decode_shift_int(encoded_int)
        for i in unshifted_int:
            print(self.messageHandler.ints_to_string(i))
        if self.debug_mode: print(f"Encoded Int : {encoded_int}")

#        self.send_msg()

    def encode_vigenere(self, msg, key):
        #msg_encoded = vigenere_encrypt(msg,key)
        msg_int = self.messageHandler.string_to_ints(msg)
        key_int = self.messageHandler.string_to_ints(key)
        msg_encoded = int_vigenere_encrypt(msg_int, key_int, self.debug_mode)
        if self.debug_mode: print(f"Encryption : {msg_encoded}")
        self.send_msg(msg_encoded, True, True)
    def decode_vigenere(self,encoded_msg, key):
        msg_decoded = vigenere_decrypt(encoded_msg,key)
        if self.debug_mode: print(f"Decryption : {msg_decoded}")
        self.send_msg(msg_decoded)

    def exit(self):
        pass

    def send_msg(self, msg, is_server=True, is_ints_list=False):
        self.messageHandler.send_message(msg, is_server, is_ints_list)

