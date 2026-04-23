import secrets
from Crypto.Util import number
import random


def find_prime_factors(n):
    factors = list()
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            if d not in factors:
                factors.append(d)
            n = n // d
        d = d+1
    if n > 1:
        if n not in factors:
            factors.append(n)
    return factors

def find_generator(p):
    if not number.isPrime(p):
        return None

    phi = p - 1
    prime_factors = find_prime_factors(phi)

    for g in range(2, p):
        is_generator = True
        for f in prime_factors:
            if pow(g, phi // f, p) == 1:
                is_generator = False
                break
        if is_generator:
            return g

    return None

def generate_prime_number(max_value):
    while True:
        n = random.randint(2, max_value)
        if number.isPrime(n):
            return n

        
def generate_private_key(p):
    return secrets.randbelow(p-3) + 2

def generate_public_key(g, private_key, p):
    return pow(g, private_key, p)

def compute_shared_key(public_key, private_key, p):
    return pow(public_key, private_key, p)

def Diffie_Hellman():
    p = generate_prime_number(2048)
    g = find_generator(p)
    #print(f"Paramètres publics: p = {p}, g = {g}")

    # Alice
    a = generate_private_key(p)
    A = generate_public_key(g, a, p)
    #print(f"Alice: clé privée a = {a}, clé publique A = {A}")

    # Bob
    b = generate_private_key(p)
    B = generate_public_key(g, b, p)
    #print(f"Bob: clé privée b = {b}, clé publique B = {B}")

    # Calcul des clés secrètes partagées
    key_alice = compute_shared_key(B, a, p)
    key_bob = compute_shared_key(A, b, p)
    """
    print(f"Clé secrète calculée par Alice: {key_alice}")
    print(f"Clé secrète calculée par Bob: {key_bob}")
    print(f"Les clés sont identiques: {key_alice == key_bob}")
    """

"""
# Test avec des valeurs fixes
def diffie_hellman_example():
    p = 23
    g = 5
    print(f"Paramètres publics: p = {p}, g = {g}")

    # Alice
    a = 6
    A = pow(g, a, p)  # A = 5^6 mod 23 = 8
    print(f"Alice: clé privée a = {a}, clé publique A = {A}")

    # Bob
    b = 15
    B = pow(g, b, p)  # B = 5^15 mod 23 = 19
    print(f"Bob: clé privée b = {b}, clé publique B = {B}")

    # Calcul des clés secrètes partagées
    key_alice = pow(B, a, p)  # K = 19^6 mod 23 = 2
    key_bob = pow(A, b, p)    # K = 8^15 mod 23 = 2

    print(f"Clé secrète calculée par Alice: {key_alice}")
    print(f"Clé secrète calculée par Bob: {key_bob}")
    print(f"Les clés sont identiques: {key_alice == key_bob}")
diffie_hellman_example()
"""