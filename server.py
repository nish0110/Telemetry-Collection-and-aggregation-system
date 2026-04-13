import socket
import ssl
import json
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# --- GENERATE SELF-SIGNED CERT (For Lab Testing) ---
if not os.path.exists("server.crt"):
    print("[*] Generating self-signed certificate...")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")])
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=365)).add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False).sign(key, hashes.SHA256())
    with open("server.key", "wb") as f: f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    with open("server.crt", "wb") as f: f.write(cert.public_bytes(serialization.Encoding.PEM))

# --- SERVER CONFIG ---
IP = "127.0.0.1" 
PORT = 5000

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP, PORT))
server_sock.listen(5)

print(f"[*] Server listening on {IP}:{PORT}...")

while True:
    client_conn, addr = server_sock.accept()
    try:
        with context.wrap_socket(client_conn, server_side=True) as secure_conn:
            print(f"[+] Connection accepted from {addr}")
            while True:
                data = secure_conn.recv(1024).decode()
                if not data: break
                
                # Handle potential multiple JSON objects in one stream
                for line in data.strip().split('\n'):
                    payload = json.loads(line)
                    print(f"[Data] Client: {payload['client_id']} | CPU: {payload['cpu']:.2f}%")
    except Exception as e:
        print(f"[!] Error: {e}")