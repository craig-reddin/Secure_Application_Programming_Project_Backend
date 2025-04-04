from functools import wraps
import secrets
import base64
import os
import jwt
import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask import request, jsonify

class EncryptionManager:
    
    
    def __init__(self):
        # Generate secret key for the session
        self.__secret_key = self.get_new_encryption_key()
    
    def initialise_encrypted_storage(self):
        #Encrypt database path database
        #Not ideal in real life scenario but valid for displaying ecryption concept put into play for a non deployed application
        iv, encrypted_route = self.__encrypt("students.db")

        #Save the variables and generated secret when initialised to variables.txt
        self.__save_to_file("variables.txt", "DATABASE_ROUTE", encrypted_route, "DATABASE_IV", iv, "SECRET_KEY", self.__secret_key)
    
    def __save_to_file(self, file_path, key1, value1, key2, value2, key3, value3 ):
        #Save encrypted key-value pairs to a file
        # Delete the file if it exists to ensure removal of old data
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Write new data to a new file
        with open(file_path, "w") as text_file:
            text_file.write(f"{key1}={value1}\n{key2}={value2}\n{key3}={value3}\n")
    
    def read_encrypted_data(self, file_path):
        #Read encrypted data from a file
        encrypted_data = {}
        try:
            with open(file_path, "r") as file:
                # Loop through each line and extract key-value pairs
                for line in file:
                    if "=" in line:
                        # Split only at first Equals sign
                        key, value = line.strip().split("=", 1)  
                        encrypted_data[key] = value
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading encrypted data: {str(e)}")
        
        return encrypted_data
    
    def __encrypt(self, message):
        #Encrypt a message using AES-CTR
        # Generate IV (Initialisation Vector)
        iv = secrets.token_bytes(16)
        
        # Create AES-CTR cipher
        algorithm = algorithms.AES(self.__secret_key)
        mode = modes.CTR(iv)
        cipher = Cipher(algorithm, mode)
        
        # Encrypt the message
        encryptor = cipher.encryptor()
        
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        encrypted_message = encryptor.update(message) + encryptor.finalize()
        
        # Encode IV and ciphertext in Base64
        encoded_iv = base64.b64encode(iv).decode('utf-8')
        encoded_ciphertext = base64.b64encode(encrypted_message).decode('utf-8')
        
        return encoded_iv, encoded_ciphertext
    
    def decrypt(self, encoded_message, encoded_iv):
        #Decrypt a message using AES-CTR
        try:
            # Decode Base64 values
            iv = base64.b64decode(encoded_iv)
            message = base64.b64decode(encoded_message)
            
            # Create AES-CTR cipher with the same secret key used to encrypt the data
            algorithm = algorithms.AES(self.__secret_key)
            mode = modes.CTR(iv) 
            cipher = Cipher(algorithm, mode)
            
            # Decrypt the message
            decryptor = cipher.decryptor()
            decrypted_message = decryptor.update(message) + decryptor.finalize()
            return decrypted_message.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return None
    
    def get_new_encryption_key(self):
        #Generate a new encryption key
        return secrets.token_bytes(32)

    
    def generate_jwt(self, email):
        #Generate a JWT token
        encrypted_data = self.read_encrypted_data("variables.txt")
        secret_key = encrypted_data.get("SECRET_KEY")
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {
            "email": email,
            "exp": expiration_time
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    
    def verify_jwt(self, token):
        #extract secret key from txt files.
        encrypted_data = self.read_encrypted_data("variables.txt")
        secret_key = encrypted_data.get("SECRET_KEY")
        #Verify a JWT
        try:
            # Decode the JWT token
            decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}
        except Exception as e:
            print(f"Error verifying JWT: {str(e)}")
            return {"error": "Internal Server Error"}

def verify_jwt(f):
    #Decorator to check JWT authentication
    #Decorator used to override calling verify_jwt in EncryptionManager class
    #Add additional functionalily before calling the  verify_jwt
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        # Create an instance of EncryptionManager
        em = EncryptionManager()
        
        # Retrieve JWT token from "Authorization" header - spelt with z purposly.
        token = request.headers.get("Authorization")
        
        # Ensure token starts with "Bearer "
        print(token)
        if token and token.startswith("Bearer "):
            #Remove bearer
            token = token.split(" ")[1] 
            print(token)
        else:
            return jsonify({"error": "Unauthorised"}), 401
        
        try:
            # Use the instance of EncryptionManager to verify the JWT
            decoded_payload = em.verify_jwt(token)
            if "error" in decoded_payload:  # If the token is invalid or expired
                return jsonify(decoded_payload), 401
            
            # Attach user data to request
            request.user = decoded_payload
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

        return f(self, *args, **kwargs)

    return decorated_function
