#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SOCK_TYPE(s)(s == SOCK_STREAM ? "Stream": s == SOCK_DGRAM ? "Datagram": s == SOCK_RAW ? "Raw": "Other")

int getaddrinfo(const char* node, const char* port, const struct addrinfo* hints, struct addrinfo** res);

const char* inet_ntop (int af, const void* src, char* dst, socklen_t size);

int main(int argc, char** argv){
	struct addrinfo hints; //hints passed to addrinfo
	struct addrinfo* results; //linked list of results populated by getaddrinfo
	struct addrinfo* res; //pointer to a result in the linked list
	char ip_address[INET_ADDRSTRLEN]; //buffer to store human-readable IP address
	
	//initialize hint and request IPv4 address
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM; //only return info for creating TCP sockets

	//attempt to resolve hostname
	int retval = getaddrinfo(argv[1], NULL, &hints, &results);
	
	if(retval){
		errx(EXIT_FAILURE, "%s", gai_strerror(retval));
	}
	for(res = results; res!=NULL; res = res->ai_next){
		struct sockaddr_in* ipv4 = (struct sockaddr_in*) res->ai_addr; //Cast result's address to a Internet socket address
		inet_ntop(res->ai_family, &ipv4->sin_addr, ip_address, sizeof(ip_address)); //convert from binary to human readable
		printf("%-15s %-10s %s\n", ip_address, SOCK_TYPE(res->ai_socktype), getprotobynumber(res->ai_protocol)->p_name);
	}

	freeaddrinfo(results);
	exit(EXIT_SUCCESS);
}


