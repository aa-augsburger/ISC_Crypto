
def resizeKey(plaintext, key):
        newKey = ""
        for i in range(len(plaintext)):
            newKey += key[i % len(key)]
        return newKey

def vigenere_encrypt(plaintext, key):
        print(f"plaintext: {plaintext}, key: {key}")

        """"Chiffre un texte caractère par caractère"""
        # Convertir le plaintext en liste de caractères
        plain_chars = list(plaintext)
        #print(f"plain_chars: {plain_chars}")

        # Redimensionner la clé
        newKey = resizeKey(plaintext, key)
        key_chars = list(newKey)
        #print(f"newKey: {newKey}, key_chars: {key_chars}")

        # Chiffrer chaque caractère
        encrypted_chars = []
        for i, char in enumerate(plain_chars):
            # Obtenir le point de code Unicode
            char_code = ord(char)
            key_code = ord(key_chars[i])

            # Addition modulo pour rester dans l'espace Unicode valide
            encrypted_code = (char_code + key_code) % 0xFFFF
            encrypted_chars.append(chr(encrypted_code))
            #print(
            #    f"char: {char}, char_code: {char_code}, key_chars: {key_chars[i]}, key_code: {key_code}, encrypted_code: {encrypted_code} == {char_code + key_code},encrypted_chars : {encrypted_chars}")
            #

        # Joindre les caractères et convertir en hexadécimal
        encrypted_text = ''.join(encrypted_chars)
        #encrypted_hex = encrypted_text.encode('utf-8')
        #print(f"encrypted_text : {encrypted_text}, encrypted_hex : {encrypted_hex}")
        return encrypted_text

def vigenere_decrypt(ciphertext, key):
        """Déchiffre un texte chiffré"""

        # Obtenir les caractères
        encrypted_chars = list(ciphertext)
        #print(f"encrypted_text : {encrypted_text}, encrypted_chars : {encrypted_chars}")

        # Redimensionner la clé
        newKey = resizeKey(ciphertext, key)
        key_chars = list(newKey)
        #print(f"newKey: {newKey}, key_chars: {key_chars}")

        # Déchiffrer chaque caractère
        decrypted_chars = []
        for i, char in enumerate(encrypted_chars):
            # Obtenir le point de code Unicode
            char_code = ord(char)
            key_code = ord(key_chars[i])
            #print(f"char: {char}, char_code: {char_code}, key_chars: {key_chars[i]}, key_code: {key_code}")

            # Soustraction modulo
            decrypted_code = (char_code - key_code) % 0xFFFF
            decrypted_chars.append(chr(decrypted_code))
            #print(f"decrypted_code: {decrypted_code} == {(char_code - key_code)}, decrypted_chars: {decrypted_chars}")

        # Joindre les caractères
        decrypted_text = ''.join(decrypted_chars)
        #print(f"decrypted_chars: {decrypted_chars} decrypted_text: {decrypted_text}")
        return decrypted_text
"""
# Test avec l'approche caractère par caractère
cipher2 = vigenere_character_algorithm()

plaintext = "nopinappleonpizza"
key = "isciscool"

encrypted2 = cipher2.vigenere_encrypt(plaintext, key)
print(f"Texte chiffré : {encrypted2}")

decrypted2 = cipher2.vigenere_decrypt(encrypted2, key)
print(f"Texte déchiffré : {decrypted2}")
"""