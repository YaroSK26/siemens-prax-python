from flask import Flask, request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json 

app = Flask(__name__)

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

public_key_str = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

data_store = {}

@app.route("/keys")
def get_keys():
    return f"{public_key_str} "

@app.route("/store", methods=['POST'])
def store_data():
    encrypted_data = request.data
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    data = json.loads(decrypted_data.decode('utf-8')) 
    data_store[data['id']] = data['key']
    return "Data stored successfully"

@app.route("/encrypt", methods=['POST'])
def encrypt_data():
    encrypted_data = request.data
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode('utf-8') 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.run()