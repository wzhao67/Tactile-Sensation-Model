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

#define SOCK_TYPE(s)(s == SOCK_STREAM ? "Stream": s == SOCK_DGRAM ? "Datagram": s == SOCK_RAW ? "Raw": "Other")
#define BACKLOG 25

static bool term_requested = false;

struct addrinfo* get_server_sockaddr(const char* port)
{
	struct addrinfo hints; //hints passed to getaddrinfo
	struct addrinfo* results; //pointer to a result in the linked list
	
	//initialize hints
	memset (&hints, 0 , sizeof(struct addrinfo));
	
	hints.ai_family = AF_INET; //return socket addresses for our local IPv4 addresses
	hints.ai_socktype = SOCK_STREAM; //return TCP socket addresses
	hints.ai_flags = AI_PASSIVE; //socket addreses should be for listening sockets
	
	int retval = getaddrinfo(NULL, port, &hints, &results);
	
	if(retval) errx(EXIT_FAILURE, "%s", gai_strerror(retval));
	
	return results;
}

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

int wait_for_connection(int sockfd)
{
	struct sockaddr_in client_addr; //remote IP that is connecting to us
	unsigned int addr_len = sizeof(struct sockaddr_in); //length of remote IP structure
	char ip_address[INET_ADDRSTRLEN]; //buffer to store human-friendly IP address
	int connectionfd; //Socket file descriptor for new connection
	
	//Wait for new connection
	connectionfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_len);
	
	//Makw sure the connection was estabished successfully
	if(connectionfd == -1) 
		err(EXIT_FAILURE, "%s", "Unable to accept connection");
	
	//Conver the connecting IP to a human friendly form and print it
	inet_ntop(client_addr.sin_family, &client_addr.sin_addr, ip_address, sizeof(ip_address));
	printf("Connection accepted from %s\n", ip_address);
	
	//Return socket file descriptor for new conection
	return connectionfd;
}

void handle_connection(int connectionfd)
{
	char buffer[4096];
	int bytes_read;
	
	do
	{
		//Read up to 4095 bytes from the client
		bytes_read = recv(connectionfd, buffer, sizeof(buffer)-1, 0);
		
		//If data was read successfully
		//THIS PART DETERMINES HOW MESSAGES ARE SEGMENTED. EG IF MESSAGES END WITH 2 NEWLINES
		//THEN RECV WILL BE CALLED UNTIL IT SEES TWO NEW LINE CHARACTERS
		if(bytes_read > 0)
		{
			//Add a terminating NULL character and print the message received
			buffer[bytes_read] = '\0';
			printf("Message reeived (%d bytes): %s \n", bytes_read, buffer);
			
			//Echo data back to client; exit loop if we'reunable to send
			if(send(connectionfd, buffer, bytes_read,0) == -1)
			{
				warn("Unable to send data to client");
				break;
			}
		}
	} while(bytes_read>0 && !term_requested);
	
	close(connectionfd);
}

void term_handler(int signal)
{
	printf("Termination requested...\n");
	term_requested = true;
}

/*
1. Call getaddrinfo to get server's socket address
2. Call socket to create a socket
3. Bind socket address to the socket with bind
4. Listen for connections with listen
5. Wait for a new connection with accept
6. Read and write with recv and send 
7. Close the connection with close
*/
int main(int argc, char** argv)
{
	//call sigaction to tell OS to call term_handler whenever Ctrl+C is pressed
	struct sigaction sa;
	sa.sa_handler = term_handler; 
	sa.sa_flags = 0;
	sigaction(SIGINT, &sa, NULL);
	
	//We want to listen on the port specified on command line
	struct addrinfo* results = get_server_sockaddr(argv[1]);
	
	//Create listening socket
	int sockfd = bind_socket(results);
	
	//Start listening on the socket
	if(listen(sockfd, BACKLOG) == -1)
		err(EXIT_FAILURE, "%s", "Unable to listen to socket.");
	
	int connectionfd;
	
	while(!term_requested)
	{
		//Wait for a connection and handle it
		connectionfd = wait_for_connection(sockfd);
		handle_connection(connectionfd);
	}
	
	//Close connection socket
	close(connectionfd);
	
	//close greeter socket and exit
	close(sockfd);
	exit(EXIT_SUCCESS);
}

