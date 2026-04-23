def hash(text):#enter a texte, it will be hashed into a 256bits word
    salt = os.urandom(16)
    combined = salt + text.encode()
    hashed = hashlib.sha256(combined).hexdigest()
    return hashed