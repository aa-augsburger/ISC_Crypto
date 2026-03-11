from MessageHandler import MessageHandler
from NetworkManager import NetworkManager

class Client:

    def __init__(self, address, port):
        self.networkManager = NetworkManager(address, port)
        self.messageHandler = MessageHandler(self.networkManager)


    def inputController(self):
        input = self.getInput()
        command = self.parseInput(input)
        print(command)

    def getInput(self):
        inp = input("Entrer votre commande : ")
        return inp

    def parseInput(self, input):
        inputTab = input.split(" ")
        match len(inputTab):
            case 0:
                self.send_msg(inputTab[0])
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

    def send_msg(self, msg):
        self.messageHandler.sendMessage(self.networkManager, msg, True)

    def help(self):
        print("Commande : /help")

    def exit(self):
        pass



