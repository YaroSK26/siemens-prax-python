from flask import Flask, jsonify, request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/data')
def data():
    try:
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        # Serialize the public key to PEM format
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Convert the PEM bytes to a base64 string for JSON serialization
        pem_str = base64.b64encode(pem).decode('utf-8')

        return jsonify({"public_key": pem_str})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        encrypted_key = base64.b64decode(request.form["key"])
        encrypted_iv = base64.b64decode(request.form["iv"])

        print(encrypted_iv)
        print(encrypted_key)

        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Decrypt AES key and IV with RSA private key
        key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        iv = private_key.decrypt(
            encrypted_iv,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        global AES_key
        global AES_iv
        AES_key = key
        AES_iv = iv

        return "Success"
    except Exception as e:
        print("Error:", e)  # Debug output
        return jsonify({"error": "Failed to decrypt data"}), 500
    
@app.route('/receive_message', methods=['POST'])
def receive_message():
    try:
        encrypted_message = base64.b64decode(request.form["content"])

        cipher = Cipher(algorithms.AES(AES_key), modes.OFB(AES_iv))
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()        
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
        
        reversed_message = decrypted_message.decode("ASCII")[::-1]
        encrypted_reversed_message = encryptor.update(reversed_message.encode("UTF-8")) + encryptor.finalize()

        return encrypted_reversed_message
    except Exception as e:
        print("Error:", e)  # Debug output
        return jsonify({"error": "Failed to decrypt data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
