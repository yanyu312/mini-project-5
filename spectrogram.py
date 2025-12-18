# tools/spectrogram.py
#
# Python helper for spectrogram (STFT)
# This script is for verification / visualization only.
# Core implementation is written in C.

import sys
import wave
import numpy as np

def read_wav(path):
    with wave.open(path, "rb") as w:
        ch = w.getnchannels()
        fs = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)

    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)

    if ch == 2:
        x = x.reshape(-1, 2).mean(axis=1)

    x /= 32768.0
    return fs, x

def window_func(name, N):
    name = name.lower()
    if name in ("rect", "rectangular"):
        return np.ones(N)
    elif name == "hamming":
        return np.hamming(N)
    else:
        raise ValueError("Unknown window type")

def main():
    if len(sys.argv) < 7:
        print("Usage:")
        print("  python spectrogram.py win_ms window_type fft_ms hop_ms input.wav output.txt")
        sys.exit(1)

    win_ms = float(sys.argv[1])
    wtype  = sys.argv[2]
    fft_ms = float(sys.argv[3])
    hop_ms = float(sys.argv[4])
    wav_in = sys.argv[5]
    txt_out = sys.argv[6]

    fs, x = read_wav(wav_in)

    win_len = int(fs * win_ms / 1000)
    hop_len = int(fs * hop_ms / 1000)
    nfft    = int(fs * fft_ms / 1000)

    win = window_func(wtype, win_len)

    frames = []
    for start in range(0, len(x) - win_len + 1, hop_len):
        frame = x[start:start + win_len] * win
        X = np.fft.rfft(frame, nfft)
        mag = np.abs(X)
        frames.append(mag)

    frames = np.array(frames)

    with open(txt_out, "w") as f:
        for frame in frames:
            f.write(" ".join(f"{v:.6f}" for v in frame))
            f.write("\n")

    print(f"Saved spectrogram to {txt_out}")

if __name__ == "__main__":
    main()
