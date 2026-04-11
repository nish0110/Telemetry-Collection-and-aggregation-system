import socket
import ssl
import json
import time
import random
import sys

SERVER_IP = "10.20.203.186"
PORT = 5000

client_id = sys.argv[1] if len(sys.argv) > 1 else "client"

context = ssl.create_default_context()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname=SERVER_IP)

secure_sock.connect((SERVER_IP, PORT))

print("Connected to server")

seq = 0

while True:

    telemetry = {
        "client_id": client_id,
        "seq": seq,
        "cpu": random.uniform(0,100),
        "memory": random.uniform(0,100)
    }

    message = json.dumps(telemetry)

    secure_sock.send(message.encode())

    seq += 1

    time.sleep(1)