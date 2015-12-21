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
#include "udp_sockets.h"
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

