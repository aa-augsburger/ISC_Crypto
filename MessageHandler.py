from NetworkManager import NetworkManager


class MessageHandler:
    def __init__(self,nm):
        print("Message Handler Initiated")
        self.networkManager = nm

    # ==========================================
    # CONSTANTS
    # ==========================================
    ISC_HEADER = b'ISC'
    BYTES_PER_CHAR = 4
    IMAGE_WIDTH = 128
    IMAGE_HEIGHT = 128


    # ==========================================
    # INT <-> BYTES CONVERSION
    # ==========================================

    #Convertir entier en octet

    def int_to_bytes(self, value, num_bytes=BYTES_PER_CHAR):
        output = value.to_bytes(num_bytes, byteorder='big')
        return output

    #Convert octet en int
    def bytes_to_int(self, data):
        try:
            output = int.from_bytes(data, byteorder='big')
        except ValueError:
            print(f"Erreur : {data}")
        return output
    # ==========================================
    # STRING <-> INTEGER LIST CONVERSION
    # ==========================================

    #convertir texte en liste de nombre
    def string_to_ints(self, text):
        output = []
        for c in text:
            output.append(ord(c)) #ord donne la valeur ascii d'un char
        return output
    #convertir liste de nombre en text utf-8
    def ints_to_string(self, int_list):
        output = ""
        for num in int_list:
            try:
                if num <= 255:
                    output += chr(num)
                else:
                    num_bytes = num.to_bytes(4, byteorder='little')
                    num_bytes = num_bytes.rstrip(b'\x00')
                    output += num_bytes.decode('utf-8')
            except ValueError:
                output += '*'
        return output

    # ==========================================
    # NETWORK ENCODING
    # ==========================================

    #stard big endians
    def encode_ints(self, int_list, byte_per_int=BYTES_PER_CHAR):
        output = []
        for num in int_list:
            output.append(self.int_to_bytes(num))
        return output

    def decode_ints(self, data, bytes_per_int=BYTES_PER_CHAR):
        output = []
        length = len(data)
        for i in range(0, length, bytes_per_int):
            chunk = data[i:i + bytes_per_int] #on découpe en chunk de 4 bits
            output.append(self.bytes_to_int(chunk))
        return output
    # ==========================================
    # TEXT ENCODING
    # ==========================================

    def encode_string(self, text):
        int_list = self.string_to_ints(text)
        output = self.encode_ints(int_list)
        return output
    # ==========================================
    # ISC MESSAGE CREATION
    # ==========================================
    #creer un message au format protocle ISC
    def create_text_message(self, text, is_server=False, bytes_per_char = BYTES_PER_CHAR):
        output = b''
        msg_type = b's' if is_server else b't'
        text_size = self.get_text_size(text)
        encoded_text = b''.join(self.encode_string(text))

        output = self.ISC_HEADER + msg_type + text_size + encoded_text

        return output

    def create_image_message(self, width, height, image_data):
        pass
    # ==========================================
    # MESSAGE RECEPTION
    # ==========================================

    #réception séquentielle :
    #ajouter les nouvelles données recu dans un buffer
    def add_data(self, msg_awaited):
        buffer = []
        msg_rcv = 0
        while msg_rcv < msg_awaited:
            data = self.networkManager.receive()
            msg = self.parse_text_message(data)
            buffer.append(msg)
            msg_rcv += 1
        return buffer
    #parcourir le buffer et extraire les messages bruts
    def get_messages(self, buffer):
        for msg in buffer:
            print(msg)
    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================

    #extraction final
    #prendre un message ISC brut et extraire le text en clair
    def parse_text_message(self, message, bytes_per_char = BYTES_PER_CHAR):
        payload = message[6:] #On ne prend pas les 6 premier 0ctet 2 * 3
        print(f"payload : {payload}")
        int_list = self.decode_ints(payload)
        output = self.ints_to_string(int_list)
        return output


    #extraire les données des pixels RGB d'un message ISC avec image dedans
    def parse_image_message(self, message):
        pass

    def get_text_size(self, text, bytes_per_char = BYTES_PER_CHAR):
        length = len(text)
        length_in_bytes = length.to_bytes(2, byteorder='big')
        return length_in_bytes

    # ==========================================
    #  MESSAGE SENDING
    # ==========================================

    def send_message(self, message, isServer=False):
        msg = self.create_text_message(message, isServer)
        self.networkManager.send(msg)