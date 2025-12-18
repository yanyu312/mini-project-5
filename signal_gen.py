# tools/signal_gen.py
import sys
import math
import wave
import struct

PI = 3.141592653589793

def s_j(t: float, f: float, j: int) -> float:
    """Same 4 waveforms as the C version."""
    if j == 0:
        # sine
        return math.sin(2 * PI * f * t)
    elif j == 1:
        # sawtooth: f*t - floor(f*t)
        return (f * t) - math.floor(f * t)
    elif j == 2:
        # square: sign(sin)
        return 1.0 if math.sin(2 * PI * f * t) >= 0 else -1.0
    elif j == 3:
        # triangle: 2*fabs(2*(f*t - floor(f*t+0.5))) - 1
        return 2.0 * abs(2.0 * (f * t - math.floor(f * t + 0.5))) - 1.0
    else:
        return 0.0

def clamp_int16(x: float) -> int:
    if x > 32767:
        return 32767
    if x < -32768:
        return -32768
    return int(x)

def main():
    # Keep the same CLI as C:
    # Usage: signal_gen.py sample_rate output.wav
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} sample_rate output.wav")
        sys.exit(1)

    fs = int(sys.argv[1])
    out_wav = sys.argv[2]

    duration = 4
    samples = fs * duration

    a = [100, 2000, 1000, 500, 250, 100, 2000, 1000, 500, 250]
    f = [0, 31.25, 500, 2000, 4000, 44, 220, 440, 1760, 3960]

    # Write WAV: mono, 16-bit PCM
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)     # 16-bit
        w.setframerate(fs)

        frames = bytearray()

        for n in range(samples):
            t = n / fs
            x = 0.0

            for j in range(4):
                for i in range(10):
                    start = 0.1 * i + j
                    end = 0.1 * (i + 1) + j
                    if start <= t < end:
                        x += a[i] * s_j(t - start, f[i], j)

            sample = clamp_int16(x)
            frames += struct.pack("<h", sample)

        w.writeframes(frames)

if __name__ == "__main__":
    main()
