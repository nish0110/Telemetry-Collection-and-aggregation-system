#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "127.0.0.1"
#define PORT 8080
#define PACKET_COUNT 10000

// FORCE 20-byte size (Removes the 24-byte error)
#pragma pack(push, 1)
typedef struct {
    uint32_t seq_num;   // 4 bytes
    double timestamp;   // 8 bytes
    float cpu_usage;    // 4 bytes
    float mem_usage;    // 4 bytes
} TelemetryPacket;
#pragma pack(pop)

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server_addr;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) return 1;

    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    
    // FIX: Using inet_addr instead of inet_pton for Windows compatibility
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    printf("Sending %d packets to %s...\n", PACKET_COUNT, SERVER_IP);

    for (uint32_t i = 0; i < PACKET_COUNT; i++) {
        TelemetryPacket packet = { i, (double)time(NULL), (float)(rand()%100), (float)(rand()%100) };
        
        sendto(sock, (const char*)&packet, sizeof(packet), 0, 
               (const struct sockaddr *)&server_addr, sizeof(server_addr));
        
        Sleep(1); 
    }

    printf("Done!\n");
    closesocket(sock);
    WSACleanup();
    return 0;
}