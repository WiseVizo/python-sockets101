import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # or ipconfig in terminal 
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!Disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(con, addr):
    print(f"[New Connection] : {addr} connected")

    connected = True
    while connected:
        msg_lenght = con.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = con.recv(msg_lenght).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print(f"[{addr}] : {msg}")
            con.send("Msg recieved...".encode(FORMAT))
        
    con.close()

def start():
    print(f"[Listening] : Server is listening at {SERVER}")
    server.listen()
    while True:
        con , addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con, addr))
        thread.start()
        print(f"[Active Connnections] : {threading.active_count() - 1}")

print("[Starting] : Server is Starting...")
start()
