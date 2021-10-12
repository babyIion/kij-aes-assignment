import socket
import select
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from base64 import b64encode

server_address = ('0.0.0.0', 6666)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        for socket in read_ready:
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                # receive data
                data = socket.recv(1024)
                if data:
                    file_name = data.decode('utf-8')
                    print("File name: ", file_name)

                    # Open the encrypted file
                    file_in = open(file_name, "rb")

                    # Import private RSA key
                    private_key = RSA.import_key(open("private.pem").read())

                    # Store the encrypted file
                    enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
                    print(b64encode(nonce).decode('utf-8'))

                    # Decrypt the session key with the private RSA key
                    cipher_rsa = PKCS1_OAEP.new(private_key)
                    session_key = cipher_rsa.decrypt(enc_session_key)

                    # Decrypt the data with the AES session key
                    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
                    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

                    # Create the decrypted file
                    d_filename = "decrypted_" + file_name.split('_', 1)[1]
                    with open(d_filename, 'wb') as df:
                        df.write(data)

                    # kirim pesan
                    message = "File has been received"
                    socket.send(bytes(message, 'utf-8'))
                else:
                    socket.close()
                    input_socket.remove(socket)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)

