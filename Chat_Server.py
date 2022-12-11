import socket
import sys
import threading
import time

server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(10)

connections = []


def disconnect(client_socket):
    connections.remove(client_socket)
    client_socket.close()

def broadcast(message, client_socket):
    encoded = str(len(message)).encode() + "\r\n\r\n".encode() + message.encode()
    for client in connections:
        if client != client_socket:
            client.send(encoded)

# log handle
def handle(client_socket):
    try:
        global chat_log
        # misal ada chat log
        if len(chat_log) > 0:
            chats = ""
            for log in chat_log:
                chats += (log + "\r\n\r\n")
            # print("Sending :" + str(len(chats)) + "\r\n\r\n" + chats)
            time.sleep(0.2)
            client_socket.send(str(len(chats)).encode() + "\r\n\r\n".encode() + chats.encode())
        else: # misal belum ada log
            client_socket.send("0\r\n\r\n".encode() + "No messages".encode())
        
        while True:
            incoming_message = ""
            data = client_socket.recv(1024)
            # misal ada client yang disconnect
            if not data:
                disconnect(client_socket)
                print("Disconnected from " + str(client_socket.getpeername()))
            
            else:
                message_len = int(data.decode().split("\r\n\r\n",1)[0])
                incoming_message += data.decode().split("\r\n\r\n",1)[1]

                while len(incoming_message) < message_len:
                    data = client_socket.recv(1024)
                    incoming_message += data.decode()
                    
                # terima pesan
                print("Received " + incoming_message + " from " + str(client_socket.getpeername()))
                chat_log.append(incoming_message)
                broadcast(incoming_message, client_socket)
    except:
        disconnect(client_socket)

try:
    chat_log = []
    while True:
        # ketika ada client yang masuk
        connection, client_address = server_socket.accept()
        connections.append(connection)
        print(connection)
        print("Connected to " + str(connection.getpeername()))

        threading.Thread(target=handle, args=(connection,)).start()
    

except KeyboardInterrupt:
    print("Closed")
    server_socket.close()
    sys.exit(0)




