

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <stdint.h> // <--- FIX 1: Added for uint32_t

#define SERVER_IP "127.0.0.1"
#define PORT 8080
#define PACKET_COUNT 10000

typedef struct {
    uint32_t seq_num;
    double timestamp;
    float cpu_usage;
    float mem_usage;
} TelemetryPacket;

int main() {
    int sock;
    struct sockaddr_in server_addr;
    
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    printf("Sending %d telemetry packets...\n", PACKET_COUNT);

    for (uint32_t i = 0; i < PACKET_COUNT; i++) {
        TelemetryPacket packet;
        packet.seq_num = i;
        packet.timestamp = (double)time(NULL);
        packet.cpu_usage = (float)(rand() % 100);
        packet.mem_usage = (float)(rand() % 100);

        sendto(sock, &packet, sizeof(packet), 0, 
               (const struct sockaddr *)&server_addr, sizeof(server_addr));
        
        // Small delay to simulate real-world interval
        usleep(1000); 
    }

    printf("Done.\n");
    close(sock);
    return 0;
}