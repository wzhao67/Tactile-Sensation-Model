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

struct addrinfo* get_sockaddr(const char* hostname, const char* port)
{
	struct addrinfo hints;
	struct addrinfo* results;
	
	memset(&hints, 0, sizeof(struct addrinfo));
	
	hints.ai_family = AF_INET; //Return socket address for the server's IPv4 address
	hints.ai_socktype = SOCK_STREAM; //return TCP socket address
	
	int retval = getaddrinfo(NULL, port, &hints, &results);
	
	if(retval)
		err(EXIT_FAILURE, "%s", gai_strerror(retval));
	
	return results;
}

int open_connection(struct addrinfo* addr_list)
{
	struct addrinfo* addr;
	int sockfd;
	
	//Iterate through each addrinfo in the list; stop when we successfully
	//connect to one
	for(addr = addr_list; addr != NULL; addr = addr->ai_next)
	{
		//Open a socket
		sockfd = socket(addr->ai_family, addr->ai_socktype, addr->ai_protocol);
		
		//Try next address if couldn't open a socket
		if(sockfd == -1)
			continue;
		
		//Stop iterating if we're able to connect to server
		//connect will connect to a port at random
		//unlike the server, a client does not have to bind to a predetermined port number
		if(connect(sockfd, addr->ai_addr, addr->ai_addrlen) != -1)
			break;
	}
	
	//Free the memory allocated to the addrinfo list
	freeaddrinfo(addr_list);
	
	//If addr is NULL, we tried every addrinfo and weren't able to connect
	if(addr == NULL)
		err(EXIT_FAILURE, "%s", "Unable to connect");
	else
		return sockfd;
}
/*
1. Call getaddrinfo to get socket address of server
2. Call socket to create a socket
3. Connct to the server with connect
4. Read write with recv and send respectively
5. Close the connection with close
*/
int main(int argc, char** argv)
{
	char* msg = "hello world\r\n"; //message to send
	char buffer[strlen(msg)+1]; //buffer to store received message, leaving space for NULL char
	
	//Connect to the server
	struct addrinfo* results = get_sockaddr("localhost", argv[1]);
	int sockfd = open_connection(results);
	
	//Send the message
	if(send(sockfd, msg, strlen(msg), 0) == -1)
		err(EXIT_FAILURE, "%s", "Unable to send");
	
	//Read the echo reply
	int bytes_read = recv(sockfd, buffer, sizeof(buffer)-1, 0);
	
	if(bytes_read == -1)
		err(EXIT_FAILURE, "%s", "Unable to read");
	
	//Add terminating NULL character to end and print it
	buffer[bytes_read] = '\0';
	printf("Data received: %s", buffer);
	
	//close the connection 
	close(sockfd);
	
	exit(EXIT_SUCCESS);
}