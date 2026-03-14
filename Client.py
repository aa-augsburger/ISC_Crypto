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
                        case "":
                            pass
                case 2:
                    match inputTab[0]:
                        case "/debug":
                            if(inputTab[1] == "on" or inputTab[1] == "true"):
                                self.debug(True)
                            else:
                                self.debug(False)
                        case "/list":
                            self.list(inputTab[1])
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
                        case "/decode":
                            match inputTab[1]:
                                case "shift":
                                    self.decode_shift(self.buffer[1], inputTab[2])
                                    msg_awaited = 1
                                    change_buffer = True
                                case "vigenere":
                                    self.decode_vigenere(self.buffer[1], inputTab[2])
                                    msg_awaited = 2
                                    change_buffer = True

        if self.debug_mode: print(f"Message attendu-s : {msg_awaited}")
        return msg_awaited, change_buffer

    def help(self):
        with open("help.txt", "r") as file:
            help_lines = file.read().split("/n")

        for line in help_lines:
            print(line)

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
        msg_encoded = shift(msg, int(shift_value))
        if self.debug_mode: print(f"Encryption : {msg_encoded}")
        self.send_msg(msg_encoded)
    def decode_shift(self,encoded_msg, shift_value):
        msg_decoded = unshift(encoded_msg,int(shift_value))
        if self.debug_mode: print(f"Encryption : {msg_decoded}")
        self.send_msg(msg_decoded)

    def encode_vigenere(self, msg, key):
        msg_encoded = vigenere_encrypt(msg,key)
        if self.debug_mode: print(f"Encryption : {msg_encoded}")
        self.send_msg(msg_encoded)
    def decode_vigenere(self,encoded_msg, key):
        msg_decoded = vigenere_decrypt(encoded_msg,key)
        if self.debug_mode: print(f"Decryption : {msg_decoded}")
        self.send_msg(msg_decoded)

    def exit(self):
        pass


    def send_msg(self, msg):
        self.messageHandler.send_message(msg, True)

