import socket
import select
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from datetime import datetime
from base64 import b64encode

def start():
    server_address = ('0.0.0.0', 6666)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    try:
        while True:
            message = sys.stdin.readline().rstrip()

            file_name = message.split(' ', 1)[1]
            # print(file_name)

            file_path = find_file(file_name)

            if file_path is None:
                print("File not found")
                break

            # print("File Path: ", file_path)

            start_time = datetime.now()
            
            # Generate private key and store it to private.pem
            key = RSA.generate(2048)
            private_key = key.export_key()
            file_out = open("private.pem", "wb")
            file_out.write(private_key)
            file_out.close()

            # Generate public key and store it to receiver.pem
            public_key = key.publickey().export_key()
            file_out = open("receiver.pem", "wb")
            file_out.write(public_key)
            file_out.close()

            with open(file_path, 'rb') as file:
                data = file.read()

            name_file_out = "encrypted_" + file_name
            file_out = open(name_file_out, "wb") # Create the encrypted file

            recipient_key = RSA.import_key(open("receiver.pem").read()) # Get the public RSA key
            session_key = get_random_bytes(16) # Generate key for AES

            # Encrypt the session key with the public RSA key
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            # Encrypt the data (file) with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            print(b64encode(cipher_aes.nonce).decode('utf-8'))
            [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
            file_out.close()

            print(name_file_out)
            client_socket.send(bytes(name_file_out, 'utf-8'))
            print("File has been sent")
            client_socket.shutdown(socket.SHUT_WR)

            received_data = client_socket.recv(1024).decode('utf-8')
            print(received_data)

            end_time = datetime.now()
            print("Duration: {}".format(end_time - start_time))

            client_socket.close()
            
    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)

def find_file(file_name):
    for root, dirs, files in os.walk('.'):
        for file in files:
            # print(file)
            if file == file_name:
                return os.path.join(root, file)
    return None

if __name__ == '__main__':
    start()