import socket

ip = socket.gethostbyname(socket.gethostname())
port = 9999

while True:
    data = input('Send Message: ')
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect((ip, port))
    server.send(data.encode('utf-8'))

    data_server = server.recv(1024).decode('utf-8')
    print("Data from Server: ",data_server)
    server.close()