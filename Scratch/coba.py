import socket
import select
import sys
import os
from datetime import datetime
from base64 import b64encode
import unittest
from aes import AES

def find_file(file_name):
    for root, dirs, files in os.walk('.'):
        for file in files:
            # print(file)
            if file == file_name:
                return os.path.join(root, file)
    return None

class test:
    def set_up(self, file_name):
        master_key = 0x2b7e151628aed2a6abf7158809cf4f3c
        self.AES = AES(master_key)

        # file_name = message.split(' ', 1)[1]
        # print(file_name)

        # file_name = "file.txt"

        file_path = find_file(file_name)

        print(file_path)

        if file_path is None:
            print("File not found")

        else:
            start_time = datetime.now()

            with open(file_path, 'rb') as file:
                data_string = file.read()
                print(data_string)

                data_string = 0x3243f6a8885a308d313198a2e0370734
                # text = text + (pad * chr(pad)).encode("utf-8")

                # data_string = data_string.encode('utf-8')
                # data_encrypt = bytes(data, 'utf-8')

            encrypted = (self.AES.encrypt(data_string)).decode('utf-8')

            print(encrypted)

            name_file_out = "encrypted_" + file_name
            file_out = open(name_file_out, "wb") # Create the encrypted file

            file_out.write(encrypted)
            file_out.close()

            end_time = datetime.now()
            print("Duration: {}".format(end_time - start_time))

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

            with open(file_path, 'rb') as file:
                data = file.read()

            name_file_out = "encrypted_" + file_name
            file_out = open(name_file_out, "wb") # Create the encrypted file

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

if __name__ == '__main__':
    # start()

    # set_up("file.txt")

    ini_test = test()

    ini_test.set_up("file.txt")
