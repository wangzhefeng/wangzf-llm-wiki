---
source_type: web
title: "Fourier Transformations for Time Series Analysis with Python"
author:
  - 
  - "[[Kyle Jones]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
created: 2026-04-06
description: "Fourier Transformations for Time Series Analysis with Python Fourier Transforms are a mathematical framework for finding hidden patterns in time series data through frequency analysis and signal …"
tags:
  - 
  - "clippings"
source_url: "https://medium.com/@kyle-t-jones/fourier-transformations-for-time-series-analysis-with-python-635747d1a35e"
published_at: 2025-01-17
related_concepts: []
---

## Fourier Transforms are a mathematical framework for finding hidden patterns in time series data through frequency analysis and signal decomposition

Time series data often contains hidden periodic patterns that are difficult to identify through direct observation. Fourier Transformations provide a mathematical framework to decompose these complex signals into their fundamental frequency components, revealing underlying patterns and cycles that might otherwise remain undetected.

The **Fourier Transform** converts a time series from the **time domain** (data as observed over time) to the **frequency domain** (data as periodic signals). Essentially, it expresses a time series as a sum of sine and cosine waves with different frequencies and amplitudes.

## Why Use Fourier Transformations in Time Series?

Financial markets use Fourier analysis to detect trading cycles and seasonal patterns in asset prices. By decomposing price movements into their frequency components, analysts can distinguish between short-term fluctuations and longer-term trends, informing trading strategies and risk management decisions.

In engineering applications, Fourier Transformations help identify machinery vibration patterns, enabling predictive maintenance before equipment failure. The frequency domain analysis reveals subtle changes in operating conditions that might be imperceptible in raw time series data.

Climate scientists employ these techniques to analyze temperature and precipitation patterns, identifying both natural cycles and potential anomalies. The ability to separate different frequency components helps distinguish between seasonal variations and longer-term climate trends.

Fourier Transformations are useful for detecting cycles, seasonality, or repeating structures in data and filtering noise.

![[raw/assets/attachments/timeseries/1*ISTGoIxrdexDd1sTAz1eLQ.gif]]

### Let’s build an example

Suppose we have a synthetic time series combining two sine waves with different frequencies.

```c
import numpy as np
import matplotlib.pyplot as plt

# Generate a time series with two frequencies
np.random.seed(42)
time = np.linspace(0, 10, 500)  # 500 time points
freq1, freq2 = 2, 5  # Frequencies in Hz
signal = np.sin(2 * np.pi * freq1 * time) + 0.5 * np.sin(2 * np.pi * freq2 * time)

# Plot the time series
plt.figure(figsize=(10, 4))
plt.plot(time, signal)
plt.title("Time Series (Combination of Two Sine Waves)")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.show()
```
![[raw/assets/attachments/timeseries/1*qRuXob3BkRRhohYbFi3rTQ.png]]

### Fourier Transform to Analyze Frequencies

Now, apply the **Fast Fourier Transform (FFT)** to extract the frequency components.

```c
# Apply Fourier Transform
fft_result = np.fft.fft(signal)

# Frequency axis
frequencies = np.fft.fftfreq(len(fft_result), d=(time[1] - time[0]))  

# Plot the magnitude spectrum
plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], np.abs(fft_result)[:len(fft_result)//2])
plt.title("Frequency Domain Representation")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.show()
```
![[raw/assets/attachments/timeseries/1*wyfZKq5phiQ6rG8PxjG-vA.png]]

### What Do We See?

The plot reveals peaks at **2 Hz** and **5 Hz**, corresponding to the two frequencies in the time series. These peaks show the dominant cycles in the data.

## Example 2: Fourier Transform on Real-World Data

Let’s use Fourier Transform to analyze a seasonal time series, such as the **airline passengers dataset**.

```c
#from sktime.datasets import load_airline
import numpy as np
import matplotlib.pyplot as plt

# Load the Airline Passengers Dataset
y = load_airline()
y = y.values

# Create time array
time = np.arange(len(y))

# Apply Fourier Transform
fft_result = np.fft.fft(y)
frequencies = np.fft.fftfreq(len(fft_result), d=1)  # Assume monthly data (d=1)

# Plot the original time series
plt.figure(figsize=(10, 4))
plt.plot(y)
plt.title("Original Airline Passenger Data")
plt.xlabel("Time")
plt.ylabel("Passengers")
plt.show()

# Plot the frequency domain
plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], np.abs(fft_result)[:len(fft_result)//2])
plt.title("Frequency Domain of Airline Passenger Data")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.savefig('time_series_passanger.png')
plt.show()
```
![[raw/assets/attachments/timeseries/1*i1h8GwnMPqgt-K6J5RMLAw.png]]

### What Does This Reveal?

The frequency-domain plot shows a clear peak corresponding to an annual seasonal cycle (frequency = 1/12 months). This confirms the known seasonality in airline passenger data.

## Example 3: Filtering Noise with Fourier Transform

We can use Fourier Transform to filter out high-frequency noise.

```c
# Add random noise to the signal
noisy_signal = y + np.random.normal(0, 50, len(y))

# Apply Fourier Transform to noisy signal
fft_result_noisy = np.fft.fft(noisy_signal)

# Filter out high frequencies
fft_filtered = fft_result_noisy.copy()
threshold = 0.1  # Adjust this threshold as needed
fft_filtered[np.abs(frequencies) > threshold] = 0

# Inverse FFT to get the filtered signal
filtered_signal = np.fft.ifft(fft_filtered)

# Plot the original, noisy, and filtered signals
plt.figure(figsize=(10, 6))
plt.plot(time, noisy_signal, label="Noisy Signal", alpha=0.5)
plt.plot(time, filtered_signal.real, label="Filtered Signal", color='red')
plt.title("Noise Filtering with Fourier Transform")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.savefig('time_series_passanger_amp.png')
plt.show()
```
![[raw/assets/attachments/timeseries/1*O-Rb8aMBFTcUsOnweUCCYw.png]]

### What Do We See?

The filtered signal closely matches the original signal, showing how Fourier Transform can effectively remove noise while preserving the key patterns.

### For Extremely Large Data: FFTW

For very large datasets or performance-critical applications, you can use **FFTW** (Fastest Fourier Transform in the West) or other specialized libraries for even faster FFT calculations.

Python’s `scipy.fft` module provides bindings for FFTW, offering improved performance for certain scenarios:

```c
from scipy.fft import fft, ifft

# Perform FFT with SciPy (uses FFTW internally for optimization)
fft_result = fft(signal)
ifft_result = ifft(fft_result)
```

### Advanced Applications

Modern applications often combine Fourier analysis with machine learning techniques. The frequency domain features extracted through Fourier Transformations serve as inputs to neural networks and other algorithms, enhancing pattern recognition and forecasting capabilities.

Signal filtering applications use Fourier Transformations to remove noise while preserving essential data characteristics. This technique proves particularly valuable in processing sensor data, where high-frequency noise can mask underlying patterns of interest.

### Implementation Considerations

While Fourier Transformations offer powerful analytical capabilities, proper implementation requires careful consideration of sampling rates, window sizes, and potential aliasing effects. The Fast Fourier Transform (FFT) algorithm provides efficient computation, but users must understand its assumptions and limitations to avoid misinterpretation of results.

### So what?

Fourier Transformations help us extract meaningful insights from raw data. Their ability to reveal hidden patterns, combined with efficient implementation through modern computing techniques, makes them essential for applications ranging from financial analysis to scientific research. As data complexity increases, these techniques become increasingly valuable for extracting actionable information from time series data.