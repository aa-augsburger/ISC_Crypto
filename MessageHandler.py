class MessageHandler:
    def __init__(self):
        print("Message Handler Initiated")

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
        output = data.fromBytes(data)
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
            output += chr(num)
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
        for byte in data:
            output.append(self.bytes_to_int(byte))
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
    def create_text_message(self, text, bytes_per_char = BYTES_PER_CHAR, is_server=False):
        encoded_text = self.
        output = self.ISC_HEADER + b't' +

    def create_image_message(slef, width, height, image_data):
        pass
    # ==========================================
    # MESSAGE RECEPTION
    # ==========================================

    #réception séquentielle :
    #ajouter les nouvelles données recu dans un buffer
    def add_data(self, data):
        pass
    #parcourir le buffer et extraire les messages bruts
    def get_messages(self):
        pass
    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================

    #extraction final
    #prendre un message ISC brut et extraire le text en clair
    def parse_text_message(self, message, bytes_per_char):
        pass

    #extraire les données des pixels RGB d'un message ISC avec image dedans
    def parse_image_message(self, message):
        print("salut")