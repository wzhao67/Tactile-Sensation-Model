#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include "udp_sockets.h"
#include "udp_server.h"
#include "calc_message.h"
/*
uint32_t calculate_sum(uint8_t* message)
{
    uint8_t operand_count = message[0]; //Read operand count from message
    uint8_t* ptr = message + 8;         //Pointer to start of operands
    uint16_t next_operand;              //Next operand
    uint32_t sum = 0;                   //Computed sum
    int i;
    
    //Iterate over the operands
    for(i=0; i<operand_count; ++i, ptr += sizeof(uint16_t))
    {
        //Copy each 16-bit operand from the message and add it to the sum
        memcpy(&next_operand, ptr, sizeof(uint16_t));
        sum += next_operand;
    }     
    
    //Return the computed sum
    return sum;
}
*/

/*
uint8_t* create_response_message(uint32_t result)
{
    //Create an 8-byte message
    uint8_t* message = (uint8_t*)malloc(8*sizeof(uint8_t));
    
    //The message contains no operands
    message[0] = 0;
    
    //Copy the result into the array, starting at byte 4,
    //since we need to skip the Reserved field
    memcpy(message+4, &result, sizeof(uint32_t));
    
    //Return the dynamically allocated message
    return message;
}
*/

message* create_response_message(calc_message* request)
{
    int i;
    
    //Create a response message and initialize it
    calc_message* response = (calc_message*)create_message();
    response->operand_count = 0;
    response->sum = 0;
    
    //Compute the sum from the client's request
    for(i=0; i<request->operand_count; ++i)
        response->sum += ntohs(request->operands[i]);
        
    //Convert the sum to network order
    response->sum = htonl(response->sum);
    
    //Set the length of the message (8 bytes of headers, no operands)
    response->length = 8;
    
    //Return the dynamically allocated message
    return (message*)response;
}
/*
int main()
{
    uint32_t result;            //Result to be returned to the client
    struct sockaddr_in addr;    //Source address and port
    socklen_t addr_len = sizeof(struct sockaddr_in);    //length of the addr structure
    uint8_t request[1024];      //Buffer to store client's request
    uint8_t* response;
    
    //Creat a socket and listen on port 5000
    int sockfd = create_server_socket("5000");
    
    //Read the next message into buffer, storing the source addresss in addr
    recvfrom(sockfd, request, sizeof(request), 0, (struct sockaddr*)&addr, &addr_len);
    
    //Computer the sum from the client's request
    result = calculate_sum(request);
    response = create_response_message(result);
    
    //Send the 8-byte result to the client
    sendto(sockfd, response, 8, 0, (struct sockaddr*)&addr, addr_len);
    free(response);
    
    //Close the socket
    close(sockfd);
    
    exit(EXIT_SUCCESS);
}
*/

int main()
{
    calc_message* request;      //Client's request message
    message* response;          //Server's response message
    host client;                //Client's address
    
    //Create a socket and listen on port 5000
    int sockfd = create_server_socket("5000");
    
    //Read tjhe request message and generate the response
    request = (calc_message*)receive_message(sockfd, &client);
    response = create_response_message(request);
    
    //Send the response and free the memory allocated to the messages
    send_message(sockfd, response, &client);
    free(request);
    free(response);
    
    //Close the socket
    close(sockfd);
    
    exit(EXIT_SUCCESS);
}
