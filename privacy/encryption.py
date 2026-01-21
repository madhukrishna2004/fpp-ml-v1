import os
from cryptography.fernet import Fernet

# 🔐 SINGLE, STABLE KEY
FERNET_KEY = os.getenv("FPP_ENCRYPTION_KEY")

if not FERNET_KEY:
    raise RuntimeError("FPP_ENCRYPTION_KEY not set")

fernet = Fernet(FERNET_KEY.encode())


def encrypt(data):
    return fernet.encrypt(str(data).encode()).decode()


def decrypt(token):
    return eval(fernet.decrypt(token.encode()).decode())
