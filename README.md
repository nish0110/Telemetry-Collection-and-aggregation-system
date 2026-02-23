# Secure Telemetry Collection and Aggregation System

## 📌 Project Overview

This project implements a secure, high-performance telemetry collection system using low-level UDP socket programming. Multiple distributed clients continuously send telemetry data to a central server. The server aggregates, analyzes, and reports statistics such as packet loss, throughput, and latency.

All communication is secured using DTLS (Datagram Transport Layer Security).

---

## 🎯 Objectives

- Implement UDP-based communication using low-level sockets
- Support multiple concurrent clients
- Ensure secure communication using DTLS
- Track sequence numbers and detect packet loss
- Aggregate and summarize telemetry data
- Perform scalability and performance evaluation

---

## 🏗 System Architecture

### Architecture Model
Client–Server Architecture (Multi-client)

### Components

1. **Telemetry Client**
   - Generates telemetry data at configurable rates
   - Adds sequence number and timestamp
   - Sends packets using UDP + DTLS

2. **Telemetry Server**
   - Listens for incoming DTLS connections
   - Receives and decrypts UDP packets
   - Tracks:
     - Packets received
     - Missing packets
     - Throughput
     - Latency
   - Periodically prints aggregated statistics

---

## 📡 Communication Protocol Design

Each telemetry packet follows the format:

| Field | Size | Description |
|-------|------|------------|
| Client ID | 4 bytes | Unique client identifier |
| Sequence Number | 8 bytes | Incrementing counter |
| Timestamp | 8 bytes | Packet send time |
| Payload Size | 2 bytes | Size of telemetry data |
| Payload | Variable | Telemetry values |

Example Payload:
CPU=72.3;MEM=41.2;TEMP=67.5

---

## 🔐 Security Implementation

- Protocol: UDP
- Security Layer: DTLS
- Certificate-based authentication
- Encrypted control and data communication

DTLS ensures:
- Confidentiality
- Integrity
- Authentication

---

## ⚙️ Concurrency Model

The server supports multiple concurrent clients using:

- Non-blocking sockets
- select()/epoll() (or threading if using Python)
- Independent per-client tracking

---

## 📊 Performance Evaluation

The system was tested under different load conditions:

| Clients | Packet Rate | Packet Loss | Throughput |
|----------|------------|------------|------------|
| 1        | 1000/sec   | 0%         | X MB/s     |
| 5        | 5000/sec   | X%         | X MB/s     |
| 10       | 20000/sec  | X%         | X MB/s     |

Metrics Measured:
- Packet loss percentage
- Average latency
- Throughput
- CPU usage

Observations:
- Increasing client count increases packet loss under high load
- Larger socket buffers reduce packet drops
- DTLS handshake introduces small initial latency

---

## 🚀 How to Run

### 1️⃣ Clone Repository
git clone https://github.com/nish0110/Telemetry-Collection-and-aggregation-system.git
cd Telemetry-Collection-and-aggregation-system

### 2️⃣ Run Server
python server.py

### 3️⃣ Run Client
C client.py

You can run multiple clients in separate terminals.

---

## 🛠 Optimizations Implemented

- Increased socket buffer size
- Non-blocking I/O
- Efficient packet parsing
- Graceful handling of:
  - Client disconnect
  - Invalid packets
  - DTLS handshake failures

---

## 📂 Repository Structure
Telemetry-Collection-and-aggregation-system/
│
├── server/
├── client/
└── README.md

---

## 👨‍💻 Authors

- Name 1
- Name 2

---

## 📌 Future Improvements

- Load balancing
- Distributed aggregation nodes
- Database storage
- Real-time dashboard visualization
