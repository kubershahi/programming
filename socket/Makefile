CC = g++-11
# CFLAGS  = -g -Wall

all:  socket.o
	$(CC) $(CFLAGS) socket.o -o file

socket.o:	socket.cpp
	$(CC) $(CFLAGS) -c socket.cpp

clean: 
	$(RM) file *.o *~