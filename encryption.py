import secrets
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

#Generate Secre Key for session
Secret_Key = secrets.token_bytes(32)  

def load_data():
    iv, route = encrypt(Secret_Key,"students.db")
    save_to_text_file("variables.txt", "DATABASE_ROUTE", route, "DATABASE_IV", iv)

def save_to_text_file(file_path, key, value, key2, value2):
    # Clears the text file before saving new encrypted data.
    # Delete the file if it exists to ensure complete removal of old data
    if os.path.exists(file_path):
        os.remove(file_path)
    # Write new data to a new file
    with open(file_path, "w") as text_file:
        text_file.write(f"{key}={value}\n{key2}={value2}\n")
    

def read_encrypted_data(file_path):
    # Reads the encrypted file path and iv from the text file.
    encrypted_data = {}
    with open(file_path, "r") as file:
        # loop through each line and extract key value pairs
        for line in file:
            if "=" in line:  
                key, value = line.strip().split("=", 1)  # Split only at first '='
                encrypted_data[key] = value
    return encrypted_data



def encrypt(key, message):
    # Generate IV (Initialisation Vector)
    initialisation_vector = secrets.token_bytes(16)

    # Create AES-CTR cipher
    algorithm = algorithms.AES(key)
    mode = modes.CTR(initialisation_vector)
    cipher = Cipher(algorithm, mode)

    # Encrypt the message
    encryptor = cipher.encryptor()

    if isinstance(message, str):
        message = message.encode('utf-8') 

    message_encrypted = encryptor.update(message) + encryptor.finalize()

    # Encode IV and ciphertext in Base64
    encoded_iv = base64.b64encode(initialisation_vector).decode('utf-8')
    encoded_ciphertext = base64.b64encode(message_encrypted).decode('utf-8')

    return encoded_iv, encoded_ciphertext 

def decrypt(key, encoded_message, encoded_iv):
    # Decode Base64 values
    iv = base64.b64decode(encoded_iv)
    message = base64.b64decode(encoded_message)

    # Create AES-CTR cipher with same secret key
    algorithm = algorithms.AES(key)
    mode = modes.CTR(iv)
    cipher = Cipher(algorithm, mode)
    # Decrypt the message
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(message) + decryptor.finalize()
    return decrypted_message.decode('utf-8')
