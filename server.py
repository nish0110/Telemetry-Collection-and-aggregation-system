import socket
import struct
import time

# Configuration
IP = "0.0.0.0"
PORT = 8080

# CHANGE HERE: Added '<' to force Little Endian and 20-byte alignment
PACKET_FORMAT = "<Idff" 

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    
    print(f"Server listening on {PORT}...")

    expected_seq = 0
    lost_packets = 0
    total_received = 0

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            
            # This will now correctly unpack exactly 20 bytes
            try:
                seq_num, timestamp, cpu, mem = struct.unpack(PACKET_FORMAT, data)
                
                # Simple packet loss tracking logic
                if seq_num > expected_seq:
                    lost_packets += (seq_num - expected_seq)
                
                total_received += 1
                expected_seq = seq_num + 1

                # Print stats every 500 packets so you can see it working
                if total_received % 500 == 0:
                    print(f"Stats from {addr}: Received={total_received}, Lost={lost_packets}, CPU={cpu:.1f}%")
            
            except struct.error:
                print(f"Received malformed packet of size {len(data)}")

    except KeyboardInterrupt:
        print("\nStopping Server...")
    finally:
        sock.close()

if __name__ == "__main__":
    start_server()