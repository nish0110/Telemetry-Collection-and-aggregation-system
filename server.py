import socket
import ssl
import threading
import json

HOST = "0.0.0.0"
PORT = 5000

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Secure Telemetry Server Running...")

clients = {}

def handle_client(conn, addr):

    print("Connected:", addr)

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break

            packet = json.loads(data.decode())

            client_id = packet["client_id"]
            seq = packet["seq"]

            if client_id not in clients:
                clients[client_id] = {"last_seq":-1,"lost":0,"received":0}

            c = clients[client_id]

            if c["last_seq"] != -1 and seq > c["last_seq"] + 1:
                c["lost"] += seq - c["last_seq"] - 1

            c["last_seq"] = seq
            c["received"] += 1

            if c["received"] % 20 == 0:
                print("\nClient:", client_id)
                print("Received:", c["received"])
                print("Lost:", c["lost"])

        except:
            break

    conn.close()
    print("Disconnected:", addr)


while True:

    client_socket, addr = server.accept()

    secure_conn = context.wrap_socket(client_socket, server_side=True)

    thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
    thread.start()