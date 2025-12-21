# loader.py
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

MAGIC = b"MLF1"

def derive_key(password: bytes, salt: bytes) -> bytes:
    return scrypt(password, salt, 32, N=2**15, r=8, p=1)

def decrypt_layers(blob: bytes, password: bytes, layers: int) -> bytes:
    for i in reversed(range(layers)):
        if blob[:4] != MAGIC:
            raise ValueError("File rusak atau bukan terenkripsi")

        salt  = blob[4:20]
        nonce = blob[20:36]
        tag   = blob[36:52]
        ct    = blob[52:]

        key = derive_key(password + str(i).encode(), salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        blob = cipher.decrypt_and_verify(ct, tag)

    return blob

# ===== MAIN =====
if __name__ == "__main__":
    password = "suki man ganteng"
    layers = 10

    with open("secret.func", "rb") as f:
        encrypted = f.read()

    source_code = decrypt_layers(encrypted, password, layers)

    namespace = {"__name__": "__main__"}
    exec(source_code, namespace)

    del source_code, encrypted
