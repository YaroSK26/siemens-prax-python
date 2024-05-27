import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

response = requests.get('http://localhost:5000/keys')

public_key_str = response.text
public_key_bytes = public_key_str.encode('utf-8')

public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())

print(public_key)

data = {"id": "123", "key": "secret", "meno": "a"}
data_bytes = json.dumps(data).encode('utf-8')

encrypted_data = public_key.encrypt(
    data_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
encrypted_data_str = base64.b64encode(encrypted_data).decode('utf-8')

response = requests.post('http://localhost:5000/store', json={'data': encrypted_data_str})
print(response.content)