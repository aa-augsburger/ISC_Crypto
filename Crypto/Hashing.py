import secrets
import os
import hashlib


def hash(password):#enter a texte, it will be hashed into a 256bits word
    salt = os.urandom(16)
    combined = salt + password.encode()
    hashed = hashlib.sha256(combined).hexdigest()
    return hashed

"""
key = "helo"
print(hash(key))
"""