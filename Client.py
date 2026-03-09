import socket
import MessageHandler


class Client():

    def __init__(self, address, port):

        #adresse et port du serveur
        self.server_adress = address
        self.server_port = 6000

        self.connect(self.server_adress, self.server_port)

    def connect(self, IP_address, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.sock.connect((IP_address, port))
            print("connected")
        except Exception as e:
            print(f"failed : {e}")


    def send(self, text):
        text = f"ISCt{len(text)}{text}"
        data = text.encode("utf-8")
        self.sock.send(data)

    # recevoir un message
    def receive(self):
        response = self.sock.recv(1024)
        decoded = response.decode("utf-8")
        print(decoded)
        return decoded



    # fermer la connection
    def close(self):
        pass




