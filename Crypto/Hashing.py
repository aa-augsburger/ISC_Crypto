import secrets
import os
import hashlib



def hash(password):
    salt = os.urandom(16)
    combined = salt + password.encode()
    hashed = hashlib.sha256(combined).hexdigest()
    return hashed


key = "helo"
print(hash(key))