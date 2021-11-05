import socket

ip = socket.gethostbyname(socket.gethostname())
port = 9999

while True:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((ip, port))
    server.listen(1)

    print("Waiting for client...")

    client, addr = server.accept()
    print("Connect from:", str(addr))

    data = client.recv(1024).decode('utf-8')
    print("Message from Client: ",data)

    resp_text = "We received"

    client.send(resp_text.encode("utf-8"))
    client.close()