import socket
import threading
ip = ''
port = 3389
server = socket.socket()
server.bind((ip,port))

server.listen(5)
client = []

def start():
    while True:
        conn,addr = server.accept()
        client.append(conn)
        print("Connect from:", addr)
        t = threading.Thread(target = send,args = (conn, ))
        t.start()
        print("--------------------------------------------------------------")


def send(fromConnection):
    try:
        while True:
            data = fromConnection.recv(4096)
            for cl in client:
                if cl != fromConnection:
                    cl.send(data)
    except:
        print("Client Disconnected")
        client[:] = []

start()
