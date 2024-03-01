import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # or ipconfig in terminal 
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!Disconnect"
IS_ACTIVE = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    global IS_ACTIVE
    while IS_ACTIVE:
        msg_lenght = client.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = client.recv(msg_lenght).decode(FORMAT)        
            print(msg)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def listen_user_input():
    global IS_ACTIVE
    while IS_ACTIVE:
        msg = input("Enter your message: ")
        
        if msg == DISCONNECT_MSG:
            IS_ACTIVE = False
        send(msg)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=listen_user_input)
send_thread.start()

send_thread.join()
receive_thread.join()

client.close()