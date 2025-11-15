CC = gcc
CFLAGS = -Wall -O2
TARGET = libc.so
SOURCE = quick_sort.c

SHARED_FLAGS = -shared -fPIC

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SHARED_FLAGS) -o $(TARGET) $(SOURCE)


clean:
	rm -f $(TARGET)

.PHONY: all clean