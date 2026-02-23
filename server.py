import socket
import struct
import time

# Configuration
IP = "0.0.0.0"
PORT = 8080
PACKET_FORMAT = "Idff"  # uint32, double, float, float

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    
    print(f"Server listening on {PORT}...")

    expected_seq = 0
    lost_packets = 0
    total_received = 0
    start_time = time.time()

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            # Unpack binary data
            seq_num, timestamp, cpu, mem = struct.unpack(PACKET_FORMAT, data)

            # Loss tracking
            if seq_num > expected_seq:
                lost_packets += (seq_num - expected_seq)
            
            total_received += 1
            expected_seq = seq_num + 1

            # Periodically report stats (every 1000 packets)
            if total_received % 1000 == 0:
                loss_rate = (lost_packets / (total_received + lost_packets)) * 100
                print(f"[{addr}] Received: {total_received} | Lost: {lost_packets} | Loss Rate: {loss_rate:.2f}%")
                print(f"Avg Stats -> CPU: {cpu:.1f}%, MEM: {mem:.1f}%")

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        sock.close()

if __name__ == "__main__":
    start_server()