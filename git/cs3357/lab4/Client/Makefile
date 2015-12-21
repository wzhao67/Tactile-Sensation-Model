CC	= gcc
CFLAGS	= -Wall -Werror -g -O0 -std=gnu11 
LFLAGS=-Wall -Werror -g

udp_client: udp_client.o ../common/udp_sockets.o
	$(CC) $(LFLAGS) -o $@ udp_client.o ../common/udp_sockets.o 

udp_client.o: udp_client.c ../common/udp_sockets.h udp_client.h
	$(CC) $(LFLAGS) -o $@ -c udp_client.c
	
../common/udp_sockets.o: ../common/udp_sockets.c ../common/udp_sockets.h
	$(CC) $(LFLAGS) -o $@ -c ../common/udp_sockets.c
	
clean:
	$(RM) udp_client *.o *~ *.*~
