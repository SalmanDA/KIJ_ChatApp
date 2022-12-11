import socket
import sys
import DES as des
import threading
import time

# input nama sama key
username  = input("Enter username: ")
key = input('Enter key: ')

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# baca log 
def read_logs():
    data = client_socket.recv(1024)
    message_len = int(data.decode().split("\r\n\r\n",1)[0])
    if message_len > 0:
        incoming_message = data.decode().split("\r\n\r\n",1)[1]

        if len(incoming_message) < message_len:
            data = client_socket.recv(message_len - len(incoming_message))
            time.sleep(0.2)
            incoming_message += data.decode()
        
        logs = incoming_message.split("\r\n\r\n")
        for log in logs:
            print(des.des().decrypt(key, log))
        print("\n")
            
    else:
        return

def handle(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected from server")
                client_socket.close()
                sys.exit(0)
            else: # terima pesan
                message_len = int(data.decode().split("\r\n\r\n",1)[0])
                incoming_message = data.decode().split("\r\n\r\n",1)[1]

                while len(incoming_message) < message_len:
                    data = client_socket.recv(1024)
                    incoming_message += data.decode()
                    
                # pesan didecrypt di sini
                print(des.des().decrypt(key, incoming_message))
                
    except:
        print("Disconnected from server")
        client_socket.close()
        sys.exit(0)

try:
    
    read_logs()
    thread = threading.Thread(target=handle, args=(client_socket,)).start()
    
    try:
        # ngirim pesan
        while True:
            message = input(username +"(You): ") # input pesan
            message = username + ": " + message  # gabung nama client dan pesannya
            message = des.addPadding(message) # tambah padding
            encrypted = des.des().encrypt(key, message) # encrypt
            time.sleep(0.1)
            sent = str(len(encrypted)) + "\r\n\r\n" + encrypted
            
            client_socket.send(sent.encode())
            
    except KeyboardInterrupt:
        print("Closed")
        client_socket.close()
        sys.exit(0)
        
       
# kalau koneksi client terputus
except KeyboardInterrupt:
    print("Disconnnected from " + str(client_socket.getpeername()))
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    sys.exit(0)