import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # or ipconfig in terminal 
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!Disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2000).decode(FORMAT))


send("hii")
input()
send(DISCONNECT_MSG)