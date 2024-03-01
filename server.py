import socket
import threading
import datetime

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # or ipconfig in terminal 
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!Disconnect"
CHAT_DATA = []
CLIENTS = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(con, addr, CHAT_DATA):
    print(f"[New Connection] : {addr} connected")
    CLIENTS.append(con)

    connected = True
    while connected:
        msg_lenght = con.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = con.recv(msg_lenght).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
                CLIENTS.remove(con)
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            CHAT_DATA.append({f"[{addr}: {formatted_time}]": msg})
            print(f"[{addr}] : {msg}")
            print(CHAT_DATA)

            broadcast()
        
    con.close()

def broadcast():
    print(f"[BroadCasting]: TO All...")
    message = str(CHAT_DATA).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    for client in CLIENTS:
        client.send(send_length)
        client.send(message)


def start():
    print(f"[Listening] : Server is listening at {SERVER}")
    server.listen()
    while True:
        con , addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con, addr, CHAT_DATA))
        thread.start()
        print(f"[Active Connnections] : {threading.active_count() - 1}")

print("[Starting] : Server is Starting...")
start()
