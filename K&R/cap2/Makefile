CC = gcc
SRCS = $(wildcard *.c)
BIN = $(patsubst %, bin/%, \
	  	$(subst .c,, $(SRCS)))

all: $(BIN)

$(BIN): bin/%: %.c
	$(CC) -o $@ $<

.PHONY :clean
clean:
	rm -f *.o
