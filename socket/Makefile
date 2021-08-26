CC = g++-11
# CFLAGS  = -g -Wall

server:  server.o
	$(CC) $(CFLAGS) server.o -o server

server.o:	server.cpp
	$(CC) $(CFLAGS) -c server.cpp

server2: server2.o
	$(CC) $(CFLAGS) server2.o -o server2

server2.o: server2.cpp
	$(CC) $(CFLAGS) -c server2.cpp

clean: 
	$(RM) file server server2 *.o *~