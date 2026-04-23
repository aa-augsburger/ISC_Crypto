import os
import hashlib

def hashing(text):
    hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return hashed