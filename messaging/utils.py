from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
        print("Key generated and saved!")

def load_key():
    with open('secret.key', 'rb') as key_file:
        return key_file.read()
    
def encrypt_message(message, key):
    f = Fernet(key)

    return f.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    f = Fernet(key)

    return f.decrypt(encrypted_message.encode()).decode()