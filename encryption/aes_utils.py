from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

KEY = get_random_bytes(16)

def encrypt_file(data):
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted = cipher.nonce + tag + ciphertext
    return base64.b64encode(encrypted)

def decrypt_file(enc_data):
    raw = base64.b64decode(enc_data)
    nonce = raw[:16]
    tag = raw[16:32]
    ciphertext = raw[32:]
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
