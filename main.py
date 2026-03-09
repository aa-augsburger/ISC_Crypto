import Client
from MessageHandler import MessageHandler

ADDRESS = "vlbelintrocrypto.hevs.ch"
PORT = 6000

if __name__ == '__main__':
    print("Welcome to ISC Crypto")
    client = Client.Client(ADDRESS, PORT)
    messageHandler = MessageHandler()

    message = messageHandler.create_text_message("Hello")
    client.send(message)
    while True:
        data = client.receive()
        print(data)

