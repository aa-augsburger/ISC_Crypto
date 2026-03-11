import NetworkManager
from MessageHandler import MessageHandler
from Client import Client

ADDRESS = "vlbelintrocrypto.hevs.ch"
PORT = 6000

if __name__ == '__main__':
    print("Welcome to ISC Crypto")
    client = Client(ADDRESS, PORT)
    while True:
        client.inputController()
        msg = client.messageHandler.get_messages()
        print(f"Message recu : {msg}")

