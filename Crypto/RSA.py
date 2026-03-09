
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
c = m^e mod n (now applied byte by byte)

Decryption
m = c^d mod n (now applied byte by byte)
"""
