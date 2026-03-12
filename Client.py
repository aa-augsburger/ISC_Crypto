from MessageHandler import MessageHandler
from NetworkManager import NetworkManager

class Client:

    def __init__(self, address, port):
        self.networkManager = NetworkManager(address, port)
        self.messageHandler = MessageHandler(self.networkManager)


    def command_controller(self):
        input = self.getInput()
        msg_awaited = self.parseInput(input)
        print(msg_awaited)
        buffer = self.messageHandler.add_data(msg_awaited)
        self.messageHandler.get_messages(buffer)
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

        return msg_awaited

    def send_command(self, msg):
        self.messageHandler.send_message(msg, True)

    def help(self):
        print("Commande  appelé: /help")

    def exit(self):
        pass



