import sys

from MessageHandler import MessageHandler
from NetworkManager import NetworkManager
from Crypto.Shift import *

class Client:

    def __init__(self, address, port):
        self.networkManager = NetworkManager(address, port)
        self.messageHandler = MessageHandler(self.networkManager)
        self.buffer = []
        self.message_list = []


    def command_controller(self):
        input = self.getInput()
        msg_awaited = self.parseInput(input)
        print(msg_awaited)
        self.buffer = self.messageHandler.add_data(msg_awaited)
        self.messageHandler.get_messages(self.buffer)

    def getInput(self):
        inp = input("Entrer votre commande : ")
        return inp

    def parseInput(self, input):
        inputTab = input.split(" ")
        msg_awaited = 0

        if(inputTab[0][0] != "/"):
            self.send_command(input)
            msg_awaited = 2
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
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                case 2:
                    pass
                case 3:
                    match inputTab[0]:
                        case "/encode":
                            match inputTab[1]:
                                case "shift":
                                    self.encode_shift(self.buffer[1], inputTab[2])
                                    msg_awaited = 1
                                case "vigenere":
                                    pass

        return msg_awaited

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
    def clearbuffer(self, clear_plain):
        self.buffer.clear()
        print("Le buffer a été supprimé")
    def show(self):
        print("=============== CONTENT OF THE BUFFER ==============")
        for msg in self.buffer:
            print(msg)
        print("=============== END BUFFER ==============")
    def list(self, n):
        pass

    def send_command(self, msg):
        self.send_msg(msg)
    def encode_shift(self, msg, shift_value):
        msg_encoded = shift(msg, int(shift_value))
        self.send_msg(msg_encoded)
    def decode_shift(self):
        pass

    def exit(self):
        pass


    def send_msg(self, msg):
        self.messageHandler.send_message(msg, True)

