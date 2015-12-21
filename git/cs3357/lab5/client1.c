#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "udp_sockets.h"
#include "udp_client.h"
#include "calc_message.h"

message* create_calc_request(uint16_t op1, uint16_t op2, uint16_t op3, uint16_t op4)
{
    //Create a 16 byte message
    calc_message* msg = (calc_message*)create_message();    //our new calc message has same size as the old
    
    //Store the operand count in the first byte of the message
    msg->operand_count = 4;
    
    //Copy the operands into the array, starting at byte 8,
    //since we need to skip the reserved and sum fields
    msg->operands[0] = htons(op1);
    msg->operands[1] = htons(op2);
    msg->operands[2] = htons(op3);
    msg->operands[3] = htons(op4);
    
    //The message is 16 bytes long (8 bytes of headers 8 bytes of operands
    msg->length = 16;
    
    //Return the dynamically allocated message
    return (message*)msg;
}

int main()
{
    host server;    //address of server
    calc_message* response;    //Response returned by the server
    
    //Create a socket to listen to port 5000
    int sockfd = create_client_socket("localhost", "5000", &server);
    
    //Encode the message to be sent
    message* request = create_calc_request(10, 20, 30, 40);
    
    //Send the 16-byte request to the server and free its memory
    send_message(sockfd, request, &server);
    free(request);
    
    //Read the response from the server
    //and convert its sum to host order
    response = (calc_message*)receive_message(sockfd, &server);
    response->sum = ntohl(response->sum);
    
    //Print the result and close the socket 
    printf("Result: %d\n", response->sum);
    close(sockfd);
    
    exit(EXIT_SUCCESS);
}

