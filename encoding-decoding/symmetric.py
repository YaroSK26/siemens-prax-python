# import os
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives import padding

# # Generujeme náhodný 256-bitový kľúč
# key = os.urandom(32)

# # Generujeme náhodný 128-bitový IV
# iv = os.urandom(16)

# # Vytvoríme šifru s použitím AES algoritmu a CBC módu
# cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

# # Vytvoríme encryptor a decryptor
# encryptor = cipher.encryptor()
# decryptor = cipher.decryptor()

# # Požiadame užívateľa o vstupný text na zašifrovanie
# data = input("Zadajte text na zašifrovanie: ").encode()

# # Vytvoríme padder a pridáme padding k dátam
# padder = padding.PKCS7(128).padder()
# padded_data = padder.update(data) + padder.finalize()

# # Zašifrujeme dáta
# ct = encryptor.update(padded_data) + encryptor.finalize()
# print("Zašifrovaný text: ", ct)

# # Dešifrujeme text
# decrypted_text = decryptor.update(ct) + decryptor.finalize()

# # Vytvoríme unpadder a odstránime padding z dešifrovaných dát
# unpadder = padding.PKCS7(128).unpadder()
# unpadded_data = unpadder.update(decrypted_text) + unpadder.finalize()

# # Vytlačíme dešifrovaný text
# print("Dešifrovaný text: ", unpadded_data.decode())


import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ct = encryptor.update(b"a secret message") + encryptor.finalize()
print(ct)
decryptor = cipher.decryptor()
a = decryptor.update(ct) + decryptor.finalize()
print(a)