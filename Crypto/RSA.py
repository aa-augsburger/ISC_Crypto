
import math
import random
"""
Key Generation from ISC Crypto course

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


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a, m)
    return (x % m + m) % m if gcd == 1 else None


def generate_small_prime():
    while True:
        p = random.randint(11, 10000)
        if is_prime(p):
            return p


def generate_keypair():
    p = generate_small_prime()
    q = generate_small_prime()
    while p == q:
        q = generate_small_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while e >= phi:
        e = random.randint(3, 100)
        if math.gcd(e, phi) != 1:
            e = 65537

    d = mod_inverse(e, phi)

    return (n, e), (n, d)


def encrypt_message_byte_by_byte(message, public_key):
    n, e = public_key
    encrypted = []

    for byte in message:
        if byte >= n:
            # should not happen if we chose n big enough
            raise ValueError(f"TOO BIG")

        enc_byte = pow(byte, e, n)
        encrypted.append(enc_byte)

    return encrypted


def decrypt_message_byte_by_byte(encrypted_bytes, private_key):
    n, d = private_key
    decrypted = []

    for enc_byte in encrypted_bytes:
        dec_byte = pow(enc_byte, d, n)
        decrypted.append(dec_byte)

    return bytes(decrypted)



public_key, private_key = generate_keypair()
print(f"Public Key (n, e): {public_key}")
print(f"Private Key (n, d): {private_key}")

message = "ISC Hello World"

print(f"Before Encrypted : {message}")

encrypted_bytes = encrypt_message_byte_by_byte(message, public_key)
print(f"After Encrypted : {encrypted_bytes}")

decrypted = decrypt_message_byte_by_byte(encrypted_bytes, private_key)
print(f"After Decrypted : {decrypted}")