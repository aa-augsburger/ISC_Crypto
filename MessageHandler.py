class MessageHandler:
    def __init__(self):
        print("Message Handler Initiated")

    # ==========================================
    # CONSTANTS
    # ==========================================
    ISC_HEADER = b'ISC'

    # ==========================================
    # INT <-> BYTES CONVERSION
    # ==========================================

    #Convertir entier en octet
    def int_to_bytes(self, value, num_bytes):


    #Convert octet en int
    def bytes_to_int(self, data):

    # ==========================================
    # STRING <-> INTEGER LIST CONVERSION
    # ==========================================

    #convertir texte en liste de nombre
    def string_to_ints(self, text):

    #convertir liste de nombre en text utf-8
    def ints_to_string(self, int_list):

    # ==========================================
    # NETWORK ENCODING
    # ==========================================

    #stard big endians
    def encode_ints(self, int_list, byte_per_int):

    def decode_ints(self, data, bytes_per_int):

    # ==========================================
    # ISC MESSAGE CREATION
    # ==========================================
    #creer un message au format protocle ISC
    def create_text_message(self, text, bytes_per_char, is_server=False):

    def create_image_message(slef, width, height, image_data):
        print("salut")
    # ==========================================
    # MESSAGE RECEPTION
    # ==========================================

    #réception séquentielle :
    #ajouter les nouvelles données recu dans un buffer
    def add_data(self, data):

    #parcourir le buffer et extraire les messages bruts
    def get_messages(self):

    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================

    #extraction final
    #prendre un message ISC brut et extraire le text en clair
    def parse_text_message(self, message, bytes_per_char):


    #extraire les données des pixels RGB d'un message ISC avec image dedans
    def parse_image_message(self, message):
        print("salut")