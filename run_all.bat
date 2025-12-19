@echo off
echo ===============================
echo MMSP Mini Project 5 - RUN ALL
echo ===============================

echo [1/5] Building project...
make

echo [2/5] Generating test signals...
.\bin\signal_gen 8000 s-8kHz.wav
.\bin\signal_gen 16000 s-16kHz.wav

echo [3/5] Preparing output folder...
mkdir out 2>nul

echo [4/5] Running spectrograms...
.\bin\spectrogram 32 hamming 64 16 s-8kHz.wav out\out1.txt
.\bin\spectrogram 32 rectangular 64 16 s-8kHz.wav out\out2.txt
.\bin\spectrogram 32 hamming 64 8 s-8kHz.wav out\out3.txt
.\bin\spectrogram 32 hamming 128 16 s-8kHz.wav out\out4.txt

echo [5/5] Generating PDFs...
python spectshow.py s-8kHz.wav out\out1.txt out\out1.pdf
python spectshow.py s-8kHz.wav out\out2.txt out\out2.pdf
python spectshow.py s-8kHz.wav out\out3.txt out\out3.pdf
python spectshow.py s-8kHz.wav out\out4.txt out\out4.pdf

echo ===============================
echo ALL DONE!
echo ===============================
pause
