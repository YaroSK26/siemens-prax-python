import requests
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64
import json     

def get_server_data():
    url = 'http://127.0.0.1:5000/data'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["public_key"]
    else:
        print(f"Failed to get data from server. Status code: {response.status_code}")

public_key_string = get_server_data()

public_key = serialization.load_pem_public_key(
        base64.b64decode(public_key_string),
        backend=default_backend()
    )

key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.OFB(iv))
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()


encryptedKey = public_key.encrypt(
    key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

encryptedIV = public_key.encrypt(
    iv,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

send_data = {
    "key" : base64.b64encode(encryptedKey),
    "iv" : base64.b64encode(encryptedIV)
}

'''
print(encryptedKey)

print(send_data)
'''

response = requests.post('http://127.0.0.1:5000/receive_data', send_data)

if response.status_code == 200:
    print(response.content)
    message = input("Encrypt message: ").encode("UTF-8")
    ct = encryptor.update(message) + encryptor.finalize()
    response = requests.post('http://127.0.0.1:5000/receive_message', {"content": base64.b64encode(ct)})
    if response.status_code == 200:
        decryptor = cipher.decryptor()
        pt = decryptor.update(response.content) + decryptor.finalize()
        print(pt)
    else:
        print(f"Failed to send data to server. Status code: {response.status_code}")
else:
    print(f"Failed to send data to server. Status code: {response.status_code}")
