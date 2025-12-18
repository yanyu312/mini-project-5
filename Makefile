CC=gcc
CFLAGS=-O2 -Wall -Wextra -std=c11
LDFLAGS=-lm

BIN_DIR=bin
OUT_DIR=out

all: $(BIN_DIR)/signal_gen $(BIN_DIR)/spectrogram

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

$(BIN_DIR)/signal_gen: src/signal_gen.c src/wav.c src/wav.h | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ src/signal_gen.c src/wav.c $(LDFLAGS)

$(BIN_DIR)/spectrogram: src/spectrogram.c src/wav.c src/fft.c src/wav.h src/fft.h | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ src/spectrogram.c src/wav.c src/fft.c $(LDFLAGS)

clean:
	rm -rf $(BIN_DIR) $(OUT_DIR) *.wav *.txt *.pdf

.PHONY: all clean

