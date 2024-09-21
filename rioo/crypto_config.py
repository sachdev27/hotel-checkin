import importlib.util
import os
from cryptography.fernet import Fernet

def decrypt_file(encrypted_file_path, output_file_path='config.py'):
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()

    fernet = Fernet(key)

    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

# Function to dynamically import the decrypted config file
def import_config(file_path):
    spec = importlib.util.spec_from_file_location("config", file_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config