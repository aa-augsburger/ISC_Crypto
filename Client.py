from MessageHandler import MessageHandler


class Client:

    def __init__(self, address, port):
        self.messageHandler = MessageHandler(address, port)


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



    def help(self):
        print("Commande : /help")




