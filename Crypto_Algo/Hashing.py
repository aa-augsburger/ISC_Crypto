import os
import hashlib
#on utilise une librarie et hash sha256
def hashing(text):
    hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return hashed