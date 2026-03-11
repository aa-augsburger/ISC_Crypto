from MessageHandler import MessageHandler
from NetworkManager import NetworkManager

class Client:

    def __init__(self, address, port):
        self.networkManager = NetworkManager(address, port)
        self.messageHandler = MessageHandler(self.networkManager)


    def input_controller(self):
        inp = self.getInput()
        self.parse_input(inp)


    def getInput(self):
        inp = input("Entrer votre commande : ")
        return inp

    def parse_input(self, input):
        input_tab = input.split(" ")
        if input_tab[0][0] != "/":
            self.send_command(input)
        else:
            match len(input_tab):
                case 1:
                    match input_tab[0]:
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

    def send_command(self, msg):
        print(f"message send {msg}")
        self.messageHandler.send_message(msg, True)
        self.messageHandler.add_data(2)
        print(f"task : {self.messageHandler.receptionBuffer[0]}")
        print(f"message : {self.messageHandler.receptionBuffer[1]}")

    def help(self):
        print("Commande : /help")

    def exit(self):
        self.networkManager.close()


