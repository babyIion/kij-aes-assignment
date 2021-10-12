import socket
import sys
import os
from datetime import datetime
from sys import getsizeof
from aes import AES

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

            # The key is built inside the AES implementation
            aes = AES()

            with open(file_path, 'rb') as file:
                data_string = file.read()

                print(data_string)
                print(getsizeof(data_string))
                print(type(data_string))

                data_string = int.from_bytes(data_string, "big")

            start_time = datetime.now()

            # Encrypt the data
            encrypted = aes.encrypt(data_string)
            encrypted = repr(encrypted).encode('utf-8')

            # Create the encrypted file
            name_file_out = "encrypted_" + file_name
            file_out = open(name_file_out, "wb")

            file_out.write(encrypted)
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
