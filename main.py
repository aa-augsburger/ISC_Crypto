import Client
from MessageHandler import MessageHandler

ADDRESS = "vlbelintrocrypto.hevs.ch"
PORT = 6000

if __name__ == '__main__':
    print("Welcome to ISC Crypto")
    client = Client.Client(ADDRESS, PORT)
    messageHandler = MessageHandler()

    message = messageHandler.create_text_message("task shift encode 6", True)
    print(message)
    client.send(message)
    while True:
        data = client.receive()
        print(f"Message recu : {messageHandler.parse_text_message(data)}")

