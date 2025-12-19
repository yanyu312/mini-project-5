import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Usage: python3 spectshow.py in_wav in_txt out_pdf

# 1. Read command-line arguments (file paths)
import sys
if len(sys.argv) != 4:
    print("Usage: python3 spectshow.py <input_wav> <input_txt> <output_pdf>")
    sys.exit(1)
in_wav = sys.argv[1]
in_txt = sys.argv[2]
out_pdf = sys.argv[3]

# 2. Read the WAV file
with wave.open(in_wav, 'rb') as w:
    nframes = w.getnframes()
    framerate = w.getframerate()
    nchannels = w.getnchannels()
    sampwidth = w.getsampwidth()
    frames = w.readframes(nframes)
# Convert audio frames to numpy array
if sampwidth == 2:  # 16-bit PCM
    samples = np.frombuffer(frames, dtype=np.int16)
elif sampwidth == 1:  # 8-bit PCM
    samples = np.frombuffer(frames, dtype=np.uint8).astype(np.int16) - 128
elif sampwidth == 4:  # 32-bit PCM
    samples = np.frombuffer(frames, dtype=np.int32)
else:
    # Fallback for unexpected sample widths (e.g., 24-bit or float PCM)
    samples = np.frombuffer(frames, dtype=np.int16)
# If stereo, take one channel
if nchannels > 1:
    samples = samples.reshape(-1, nchannels)[:, 0]
# Normalize samples to float [-1, 1] range (if integer)
if sampwidth == 2:
    samples = samples.astype(np.float64) / 32768.0
elif sampwidth == 1:
    samples = samples.astype(np.float64) / 128.0
elif sampwidth == 4:
    samples = samples.astype(np.float64) / 2147483648.0

# 3. Read spectrogram data from text file
spect_data = np.loadtxt(in_txt)
if spect_data.ndim == 1:
    spect_data = spect_data[np.newaxis, :]  # handle case of single frame
time_frames, freq_bins = spect_data.shape

# 4. Create waveform plot
duration = nframes / float(framerate)
time_axis = np.linspace(0, duration, num=nframes, endpoint=False)
fig1, ax1 = plt.subplots()
ax1.plot(time_axis, samples, color='blue')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.set_title("Waveform")

# 5. Create spectrogram plot
fig2, ax2 = plt.subplots()
# Transpose to get frequency × time for plotting
spect_T = spect_data.T
nyquist = framerate / 2.0
img = ax2.imshow(spect_T, aspect='auto', origin='lower',
                 extent=[0, duration, 0, nyquist], cmap='viridis')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")
ax2.set_title("Spectrogram")
# Optionally add colorbar
# cbar = fig2.colorbar(img, ax=ax2)
# cbar.set_label("Magnitude")

# 6. Save both plots into a single PDF
with PdfPages(out_pdf) as pdf:
    pdf.savefig(fig1)
    pdf.savefig(fig2)
# (The PDF now contains two pages: waveform followed by spectrogram)
