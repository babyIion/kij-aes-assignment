import socket
import sys
import os
from datetime import datetime
from base64 import b64encode
import random
from sys import getsizeof
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

        self.AES = AES()

        # file_name = message.split(' ', 1)[1]
        # print(file_name)

        file_path = find_file(file_name)

        print(file_path)

        if file_path is None:
            print("File not found")

        else:
            start_time = datetime.now()

            with open(file_path, 'rb') as file:
                data_string = file.read()
                # data_string = repr(data_string).encode('utf-8')
                # data_string = b64encode(data_string).decode('utf-8')

                print(data_string)
                print(getsizeof(data_string))
                print(type(data_string))

                data_string = int.from_bytes(data_string, "big")

            encrypted = self.AES.encrypt(data_string)
            encrypted = repr(encrypted).encode('utf-8')

            print(encrypted)

            # Create the encrypted file
            name_file_out = "encrypted_" + file_name
            file_out = open(name_file_out, "wb")

            file_out.write(encrypted)
            file_out.close()

            print("DONE ENCRYPTION")

            # =========================================

            with open('receiver.pem', 'rb') as file:
                master_key = int.from_bytes(file.read(), byteorder='big')

            file_path = find_file(name_file_out)

            with open(file_path, 'rb') as file:
                data_decrypt = file.read()
                # data_string = repr(data_string).encode('utf-8')
                # data_string = b64encode(data_string).decode('utf-8')

                print(data_decrypt)
                print(getsizeof(data_decrypt))
                print(type(data_decrypt))

                data_decrypt = int.from_bytes(data_decrypt, "big")

            decrypted = self.AES.decrypt(data_decrypt)
            decrypted = repr(decrypted).encode('utf-8')

            print(decrypted)

            # Create the decrypted file
            name_file_out = "decrypted_" + file_name
            file_out = open(name_file_out, "wb")

            file_out.write(decrypted)
            file_out.close()

            end_time = datetime.now()
            print("Duration: {}".format(end_time - start_time))

if __name__ == '__main__':
    ini_test = test()

    ini_test.set_up("file.txt")
