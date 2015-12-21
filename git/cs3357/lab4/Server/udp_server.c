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
#include "../common/udp_sockets.h"
#include "udp_server.h"

int bind_socket(struct addrinfo* addr_list)
{
	struct addrinfo* addr;
	int sockfd;
	char yes = '1';
	
	//Iterate over the addresses in the list; stop when we successfully bind to one
	for(addr = addr_list; addr != NULL; addr = addr->ai_next)
	{
		//OPen the socket
		sockfd = socket(addr->ai_family, addr->ai_socktype, addr->ai_protocol);
		
		//Move to next address if can;t
		if(sockfd == -1)
			continue;
		
		//Allow port to be re-used if currently in TIME_WAIT state
		if(setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1)
			err(EXIT_FAILURE, "%s", "Unable to set socket option");
		
		//try bind the socket to the address/port
		if(bind(sockfd, addr->ai_addr, addr->ai_addrlen)==-1)
		{
			//if binding fails, close the socket and move to next address
			close(sockfd);
			continue;
		}
		else{
			break; //successfully bound to socket
		}
	}
	//Free memory allocated to address list
	freeaddrinfo(addr_list);
	
	//If addr is NULL, we tried every address and weren't able to bind
	if(addr == NULL) err(EXIT_FAILURE, "%s", "Unable to bind");
	else  return sockfd;
}

int create_server_socket(char* port)
{
    struct addrinfo* results = get_udp_sockaddr(NULL, port, AI_PASSIVE);
    int sockfd = bind_socket(results);
    
    return sockfd;
}

/*
1. Call getaddrinfo to get server's socket address
2. Call socket to create a socket
3. Bind socket address to the socket with bind
4. Wait for messages with recvfrom
5. Send messages with sendto
6. Close the socket with close
*/

int main()
{
    message* msg;       //Message received
    host source;        //Source of the message received
    
    //Create a socket to listen on port 5000
    int sockfd = create_server_socket("5000");
    
    //Read the next message
    msg = receive_message(sockfd, &source);
    
    if(msg != NULL)
    {
        //Add NULL terminator
        msg->buffer[msg->length] = '\0';
        printf("Message received from %s: %s\n", source.friendly_ip, msg->buffer);
    }
    
    //Echo message back to the client
    if(send_message(sockfd, msg, &source) == -1)
    {
        free(msg);
        perror("Unable to send to socket");
        exit(EXIT_FAILURE);
    }
    
    //Free memory allocated to the message
    free(msg);
    
    //close the socket
    close(sockfd);
    exit(EXIT_SUCCESS);
}
