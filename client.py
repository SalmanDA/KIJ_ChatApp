import socket
import sys
import threading
import DES
import rsa
import time
import os
import key_gen

def read_msg(sock):
    while True:
        data = sock.recv(65535)
        if len(data) == 0:
            break
        data = data.decode("utf-8")
        if len(data.split(',')) == 3:
            user, msg , enc_key= data.split(',')

            print("\n\n-----Receiving Message-----")
            print("\nMessage before decrypted: " + msg) # Message sebelum di-decrypt
            msg_key = rsa.decrypt(d, N, enc_key)
            msg_key = msg_key.replace(" ","")
            # key_rev = msg_key.split()[::-1]
            print("msg_key: " + msg_key)
            print("After decrypted:")
            msg = DES.des().decrypt(msg_key, msg) # Decrypt Message
            print("(" + user + ")" + " : " + msg) # Ubah message menjadi string
            print("\nInput username destination : ")
        else:
            print("\n"+data)
            
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 6666))
sock.send(bytes(sys.argv[1], "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock,))
thread_cli.start()

key = DES.random_keys() #des key
print("key: " + key)

e, d, N = rsa.genereateKeys(16)
keypath = os.getcwd() + '\\key'
key_folder = os.listdir(keypath)
f = open(keypath+'\\'+sys.argv[1]+'.txt', 'w+')
f.write(str(e)+" "+str(N))
f.close()

# rkb = []
# DES.init_keys(key, rkb)

while True:
    dest = input("Input username destination : ")
    key_folder = os.listdir(keypath)
    if dest+'.txt' not in key_folder:
        print(dest + ' is not on client list')
    else :
        f = open(keypath+'\\'+dest+'.txt', 'r')
        recv_e, recv_N= f.read().split()
        enc_key = rsa.encrypt(int(recv_e), int(recv_N), ' '.join(map(str, key)))
        msg = input("Input message :")
        if len(msg) % 8 != 0:
            msg = DES.addPadding(msg)
            # msg = DES.ascii2bin(msg) # Ubah message menjadi binary
        cipher_text = DES.des().encrypt(key, msg) # Encrypt message dengan DES
        print("Encrypted message: " + cipher_text) # Message setelah di-encrypt
        sock.send(bytes("{}|{}|{}".format(dest, cipher_text, enc_key), "utf-8"))

        time.sleep(0.5)
