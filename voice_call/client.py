import socket
import threading
import pyaudio

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '34.146.3.246'
port = 3389

client.connect((ip, port))
print("Connect -->",ip)

p = pyaudio.PyAudio()
Format = pyaudio.paInt16
Chunks = 4096
Channels = 2
Rate = 44100

input_stream = p.open(format = Format,channels = Channels, rate = Rate, input = True, frames_per_buffer = Chunks)
output_stream = p.open(format = Format,channels = Channels, rate = Rate, output = True, frames_per_buffer = Chunks)

def send():
    while True:
        try:
            print("Sending Audio...")
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            data = input_stream.read(Chunks)
            client.send(data)
        except:
            break
def receive():
    while True:
        try:
            print("Receive Audio...")
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            data = client.recv(Chunks)
            output_stream.write(data)
        except:
            break

t1 = threading.Thread(target = send)
t2 = threading.Thread(target = receive)

t1.start()
t2.start()

t1.join()
t2.join()

input_stream.close()
output_stream.close()