from MessageHandler import MessageHandler
from NetworkManager import NetworkManager
from Crypto.Ceasar import *
from Crypto.Vigenere import *

class Client:

    def __init__(self, address, port):
        self.networkManager = NetworkManager(address, port)
        self.messageHandler = MessageHandler(self.networkManager)
        self.buffer = []


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
                case 0:
                    pass
                case 1:
                    match inputTab[0]:
                        case "/help":
                            self.help()
                        case "/health":
                            pass
                        case "/exit"  | "/quit" | "/q":
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
                        case "":
                            pass
                        case "":
                            pass
                        case "":
                            pass
                case 3:
                    match inputTab[0]:
                        case "encode":
                            match inputTab[1]:
                                case "shift":
                                    self.encode_shift(self.buffer[1], inputTab[2])
                                    msg_awaited = 1
                                case "vigenere":
                                    self.encode_vigenere(self.buffer[1], inputTab[2])
                                    msg_awaited = 1
                        case "decode":
                            match inputTab[1]:
                                case "shift":
                                    self.decode_shift(self.buffer[1], inputTab[2])
                                    msg_awaited = 1
                                case "vigenere":
                                    self.decode_vigenere(self.buffer[1], inputTab[2])
                                    msg_awaited = 1        

        return msg_awaited

    def send_command(self, msg):
        self.send_msg(msg)

    def encode_shift(self, msg, shift_value):
        msg_encoded = shift(msg, shift_value)
        self.send_msg(msg_encoded)
    def decode_shift(self,encoded_msg, shift_value):
        msg_decoded = unshift(encoded_msg,shift_value)
        self.send_msg(msg_decoded)

    def encode_vigenere(self, msg, key):
        msg_encoded = vigenere_encrypt(msg,key)
        self.send_msg(msg_encoded)
    def decode_vigenere(self,encoded_msg, key):
        msg_decoded = vigenere_decrypt(encoded_msg,key)
        self.send_msg(msg_decoded)

    def help(self):
        with open("help.txt", "r") as file:
            help_lines = file.read().split("/n")

        for line in help_lines:
            print(line)

    def exit(self):
        pass


    def send_msg(self, msg):
        self.messageHandler.send_message(msg, True)

