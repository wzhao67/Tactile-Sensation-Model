#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <signal.h>
#include <unistd.h>
#include "udp_client.h"
#include "../common/udp_sockets.h"

int create_client_socket(char* hostname, char* port, host* server)
{
    int sockfd;
    struct addrinfo* addr;
    struct addrinfo* results = get_udp_sockaddr(hostname, port, 0);
    
    //Iterate through each addrinfo in the list;
    //stop when we successfully create a socket
    for(addr = results; addr != NULL; addr = addr->ai_next)
    {
        //Open a socket
        sockfd = socket(addr->ai_family, addr->ai_socktype, addr->ai_protocol);
        
        //Try the next address if we couldn't open a socket
        if(sockfd == -1)
            continue;
           
        //Copy server address and length to the server out parameter 'server'
        memcpy(&server->addr, addr->ai_addr, addr->ai_addrlen);
        memcpy(&server->addr_len, &addr->ai_addrlen, sizeof(addr->ai_addrlen));
        
        //We have successfully created a socket; stop iterating
        break;
    }
    
    //Free the memory allocated to the addrinfo list
    freeaddrinfo(results);
    
    //If we tried every addrinfo and failed to create a socket
    if(addr == NULL)
    {
        perror("Unable to create socket");
        exit(EXIT_FAILURE);
    }
    else
    {
        //Otherwise, return the socket descriptor
        return sockfd;
    }
}

int main()
{
    host server;    //server address
    message* msg;   //message to send/receive
    
    //Create a socket for communication with the server
    int sockfd = create_client_socket("localhost", "5000", &server);
    
    //Create a message, and initialize its contents
    msg = create_message();
    msg->length = strlen("hello");
    memcpy(msg->buffer, "hello", msg->length);
    
    //Send message to server, and free its memory
    int retval = send_message(sockfd, msg, &server);
    free(msg);
    
    //If we couldn't send the message, exit the program
    if(retval == -1)
    {
        close(sockfd);
        perror("Unable to send to socket");
        exit(EXIT_FAILURE);
    }
    
    //Read the server's reply
    msg = receive_message(sockfd, &server);
    
    if(msg != NULL)
    {
        //Add NULL terminator and print reply
        msg->buffer[msg->length] = '\0';
        printf("Reply from server %s: %s\n", server.friendly_ip, msg->buffer);
        
        //Free memory allocated to the message
        free(msg);
    }
    
    //Close the socket
    close(sockfd);
    exit(EXIT_SUCCESS);
}
