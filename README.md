# Multimedia Mini Project 5

本專案包含使用 C 語言產生波形訊號（signal_gen.c），以及使用 Python 畫出該聲音的 waveform 與 spectrogram（spectrogram.py）。

## 檔案內容

* `signal_gen.c`: C 語言編寫，用來產生包含四種波形（sine, sawtooth, square, triangle）的聲音信號，並儲存為 WAV 檔案。
* `spectrogram.py`: 使用 Matplotlib 顯示 `.wav` 檔案的 waveform 與搭配文字格式的 spectrogram（ASCII），並輸出成 PDF。

## 使用方式

### 編譯 C 程式

```bash
gcc signal_gen.c -o signal_gen.exe -lm
```

### 產生 WAV 聲音

```bash
./signal_gen.exe 16000 s-16kHz.wav
./signal_gen.exe 8000 s-8kHz.wav
```

### 使用 Spectrogram 程式產生頻譜文字檔

```bash
./spectrogram.exe 32 rectangular 32 10 s-8kHz.wav s-8kHz.Set1.txt
```

### 使用 Python 顯示 Waveform 與 Spectrogram 並輸出 PDF

```bash
python3 spectrogram.py s-8kHz.wav s-8kHz.Set1.txt out.pdf
```

## 相依套件

* Python 3
* numpy
* matplotlib

安裝方式：

```bash
pip install numpy matplotlib
```

## 清理產生的檔案（如有使用 Makefile）

```bash
make clean
```

## 備註

若 spectrogram 為自行撰寫的 C 程式，請確保其能輸出與 `spectrogram.py` 相容的純文字檔案格式。

---

## Report Section

### 1. Division of Labor

* 組員 A：撰寫 `signal_gen.c`、設計波形組成邏輯。
* 組員 B：撰寫 `spectrogram.c` 與 C 語言的 FFT 實作。
* 陳彥妤/411186038：撰寫 Python 的 `spectshow.py`，完成 waveform 與 spectrogram 視覺化。
* 全體組員共同撰寫本報告與討論。

### 2. Comparison of Settings 1–4

* 各設定的差異包含：

  * Window type（如 Hamming vs. rectangular）
  * Window size（w_size）
  * DFT size（dft_size）
  * Hop size（frame interval）
* 結果差異討論：

  * Hamming window 能有效抑制旁瓣 (side lobes)，但頻率解析度稍降。
  * 窗長愈大，頻率解析度愈好；窗長愈短，時間解析度愈佳。
  * 較小 hop size 使得圖像較平滑但處理量增加。
  * Settings 1–4 展現出在不同 window 與 DFT 參數下頻譜清晰度與細節的不同。

### 3. Computation per Frame

* 假設 DFT size 為 N：

  * Complex multiplications: (N/2) * log₂(N)
  * Complex additions: N * log₂(N)
* 舉例 N = 512：

  * Multiplications ≈ 128 × 9 = 1152
  * Additions ≈ 512 × 9 = 4608
* 每一幀都會重複此計算，若 hop size 小，總 frame 數會增加。

### 4. Thoughts and Reflections

* 本次專題幫助我們更深入了解時頻分析與 FFT 實作原理。
* 實際撰寫 spectrogram 函數時需考慮視窗函數的選擇與 padding 問題。
* 將 C 語言與 Python 結合，能兼顧效率與可視化，提升理解與驗證效率。
* 團隊合作過程中，也培養了分工與整合的能力。
