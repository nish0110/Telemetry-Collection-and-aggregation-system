#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <winsock2.h>  // Required for Windows networking
#include <ws2tcpip.h>  // Required for modern IP functions

// Tell the compiler to link the Winsock library
#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "127.0.0.1"
#define PORT 8080
#define PACKET_COUNT 10000

// Use #pragma pack(1) to ensure the struct size is 20 bytes 
// exactly (essential for Python compatibility)
#pragma pack(push, 1)
typedef struct {
    uint32_t seq_num;
    double timestamp;
    float cpu_usage;
    float mem_usage;
} TelemetryPacket;
#pragma pack(pop)

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server_addr;

    // 1. Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup failed. Error Code: %d\n", WSAGetLastError());
        return 1;
    }

    // 2. Create Socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == INVALID_SOCKET) {
        printf("Socket creation failed. Error Code: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    // 3. Setup Server Address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    printf("Windows Telemetry Client started. Sending %d packets...\n", PACKET_COUNT);

    srand((unsigned int)time(NULL));

    for (uint32_t i = 0; i < PACKET_COUNT; i++) {
        TelemetryPacket packet;
        packet.seq_num = i;
        packet.timestamp = (double)time(NULL);
        packet.cpu_usage = (float)(rand() % 100);
        packet.mem_usage = (float)(rand() % 100);

        int result = sendto(sock, (const char*)&packet, sizeof(packet), 0, 
                            (const struct sockaddr *)&server_addr, sizeof(server_addr));
        
        if (result == SOCKET_ERROR) {
            printf("Send failed. Error Code: %d\n", WSAGetLastError());
            break;
        }

        // Sleep(1) = 1 millisecond (replaces usleep(1000))
        Sleep(1); 
    }

    printf("Transmission complete.\n");

    // 4. Cleanup
    closesocket(sock);
    WSACleanup();

    return 0;
}