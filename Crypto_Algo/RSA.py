
import math
import random
from MessageHandler import MessageHandler

"""
Key Generation from ISC Crypto_Algo course

Select two distinct prime numbers (p and q)
Calculate n = p × q
Calculate φ(n) = (p-1) × (q-1)
Choose an integer e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
Calculate d, the modular inverse of e modulo φ(n), i.e., d × e ≡ 1 (mod φ(n))
Public key is (n, e)
Private key is (n, d)

Encryption
c = m^e mod n (applied byte by byte)

Decryption
m = c^d mod n (applied byte by byte)
"""

#permet de verifier si un nombre est premier
def is_prime(n):
    if n <= 1:                      #cas triviaux
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:      #test si n est un diviseur de 2 ou de 3
        return False
    i = 5                   #on commence a 5
    while i * i <= n: #on test  jusqua a la racine carré de n
        if n % i == 0 or n % (i + 2) == 0:      #(test de 5 et de 7) diviseur de notre nombre
            return False
        i += 6  #on passe à 11 (test 11 et 13) est diviseur de notre n et ainsi de suite
    return True

""""#identité de bézout : ax + by = pgcd(a,b)
PSEUDO CODE ALGO EUCLIDE ETENDU TROUVE SUR WIKIPEDIA
Entrée : a, b entiers (naturels)
Sortie : r entier (naturel) et  u, v entiers relatifs tels que r = pgcd(a, b) et r = a*u+b*v

Initialisation : (r, u, v, r', u', v') := (a, 1, 0, b, 0, 1)
                  q  quotient entier

les égalités r = a*u+b*v et r' = a*u'+b*v' sont des invariants de boucle

tant que (r' ≠ 0) faire
    q := r÷r' 
    (r, u, v, r', u', v') := (r', u', v', r - q *r', u - q*u', v - q*v')
    fait
renvoyer (r, u, v)
PGCD = (nb * coef_nb + (mod * coef_mod)
On veut 1 = (nb * coef_nb + (mod * coef_mod)
"""
def euclid_extended_algo(nb, mod):
    reste, coeff, v = nb, 1, 0
    reste_prime, coeff_prime, v_prime = mod, 0, 1
    q  = 0

    while reste_prime != 0:
        q = reste // reste_prime
        reste, coeff, v, reste_prime, coeff_prime, v_prime = reste_prime, coeff_prime, v_prime, reste-q*reste_prime, coeff-q*coeff_prime, v-q*v_prime
    return (reste,coeff)

#permet de calculer la cle privé
def private_key_calculator(public_exp, phi):
    reste, coeff = euclid_extended_algo(public_exp, phi) #la cle privé est l'inverse modulaire de la cle publique dans un anneau de taille phi
    if coeff < 0: # si le nombre est négatif, on la met dans le nombre positif en lui ajoutant un tour dhorloge phi -3h egal +9h sur horloge
        coeff = coeff + phi
    return coeff



def generate_small_prime():
    while True:
        p = random.randint(11, 10000)
        if is_prime(p):
            return p

#generer la paire de cle RSA
def generate_keypair():
    p = generate_small_prime()
    q = generate_small_prime()
    while p == q:
        q = generate_small_prime()

    mod = p * q     #botre modulo
    phi = (p - 1) * (q - 1) #phi est la fonction indicatrice Euler

    public_exp = 65537
    while public_exp >= phi:        #on test si public_exp et phi nont pas de diviseur commun
        public_exp = random.randint(3, 100)
        if math.gcd(public_exp, phi) != 1:
            public_exp = 65537

    private_exp = private_key_calculator(public_exp, phi)

    return (mod, public_exp), (mod, private_exp)


def encrypt_RSA(message, public_key):
    mod, public_exp = public_key
    encrypted = []

#on parcours chaque nombre qui constitue le message
    for nb in message:
        if nb >= mod:
            # should not happen if we chose n big enough
            raise ValueError(f"TOO BIG")

        enc_byte = pow(nb, public_exp, mod) #fonction pour exponentiation modulaire built in de python pour la performance
        encrypted.append(enc_byte)

    return encrypted


def decrypt_RSA(encrypted_int_list, private_key):
    mod, private_exp = private_key
    decrypted = []

    for enc_byte in encrypted_int_list:
        dec_byte = pow(enc_byte, private_exp, mod)
        decrypted.append(dec_byte)

    return bytes(decrypted)






#=====================================================================================
#                                       TEST
#=====================================================================================
"""
def string_to_ints(text):
    output = []
    for c in text:
        utf8_bytes = c.encode('utf-8')
        num = int.from_bytes(utf8_bytes, byteorder='little')
        output.append(num)
    return output

#convertir liste de nombre en text utf-8
def ints_to_string(int_list):
    output = ""
    for num in int_list:
        try:
            num_bytes = num.to_bytes(4, byteorder='little')
            num_bytes = num_bytes.rstrip(b'\x00')
            output += num_bytes.decode('utf-8')
        except ValueError:
            output += '*'
    return output


public_key, private_key = generate_keypair()
print(f"Public Key (n, e): {public_key}")
print(f"Private Key (n, d): {private_key}")

message = "ISC Hello World"
int_message = string_to_ints(message)

print(f"Before Encrypted : {message}")

encrypted_bytes = encrypt_message_byte_by_byte(int_message, public_key)
print(f"After Encrypted : {encrypted_bytes}")

decrypted = decrypt_message_byte_by_byte(encrypted_bytes, private_key)
msg_decrypted = ints_to_string(decrypted)
print(f"After Decrypted : {msg_decrypted}")
"""