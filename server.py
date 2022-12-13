import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli, userlist):
    while True:
        data = sock_cli.recv(65535)
        print(data)
        if len(data) == 0:
            break
        msg = data.decode("utf-8").split("|")
        if msg[0] == username_cli:
            continue
        if msg[0] not in userlist:
            send_msg(sock_cli, msg[0] + " username not found")
        else:
            sendmsg = "({}): {}".format(username_cli, msg[1])
            # print(sendmsg)
            sendmsg = "{},{},{}".format(username_cli, msg[1], msg[2])
            send_msg(clients[msg[0]][0], sendmsg)
    sock_cli.close()
    print("Connection closed", addr_cli)
    userlist.remove(username_cli)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(("0.0.0.0", 6666))
sock_server.listen(5)

clients = {}
userlist = []

while True:
    sock_cli, addr_cli = sock_server.accept()

    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli, " joined")
    userlist.append(username_cli)

    thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli, userlist))
    thread_cli.start()

    clients[username_cli] = (sock_cli, addr_cli, thread_cli)