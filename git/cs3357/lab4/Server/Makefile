CC	= gcc
CFLAGS	= -Wall -Werror -g -O0 -std=gnu11 
LFLAGS=-Wall -Werror -g

udp_server: udp_server.o ../common/udp_sockets.o
	$(CC) $(LFLAGS) -o $@ udp_server.o ../common/udp_sockets.o 

udp_server.o: udp_server.c ../common/udp_sockets.h udp_server.h
	$(CC) $(LFLAGS) -o $@ -c udp_server.c

../common/udp_sockets.o: ../common/udp_sockets.c ../common/udp_sockets.h
	$(CC) $(LFLAGS) -o $@ -c ../common/udp_sockets.c
	
clean:
	$(RM) udp_server *.o *~ *.*~
