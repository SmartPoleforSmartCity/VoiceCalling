import socket
import threading

server = socket.socket()
port = 9999
server.bind(('192.168.43.173',82))

server.listen(5)
client = []

def start():
    conn,addr = socket.socket()
    client.append(conn)
    t = threading.Thread(target = sead,args = (conn, ))
    t.start()

def send(fromConnection):
    try:
        while True:
            data = fromConnection.recv(4096)
            for cl in client:
                if cl != fromConnection:
                    cl.send(data)
    except:
        print("Client Disconnected")
