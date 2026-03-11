import socket



class NetworkManager():

    def __init__(self, address, port):

        #adresse et port du serveur
        self.sock = None
        self.server_adress = address
        self.server_port = port

        self.connect(self.server_adress, self.server_port)

    def connect(self, IP_address, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.sock.connect((IP_address, port))
            print("connected")
        except Exception as e:
            print(f"failed : {e}")


    def send(self, data):
        self.sock.send(data)

    # recevoir un message
    def receive(self):
        response = self.sock.recv(1024)
        return response



    # fermer la connection
    def close(self):
        self.sock.close()




