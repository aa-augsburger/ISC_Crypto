import socket
import MessageHandler

#adresse et port du serveur
server_adress = "vlbelintrocrypto.hevs.ch"
server_port = 6000

class Client():
    def __init__(self):
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_adress, server_port))


    def send(self, text):
        data = text

        self.sock.send(data)

#recevoir un message
    # def receive(self):
    #
    #

    #ferner la connection
    # def close(self):
    #




