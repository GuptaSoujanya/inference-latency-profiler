# inference-latency-profiler

[![CI](https://github.com/GuptaSoujanya/inference-latency-profiler/actions/workflows/ci.yml/badge.svg)](https://github.com/GuptaSoujanya/inference-latency-profiler/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A high-precision, low-overhead latency and throughput profiler engineered for local and remote LLM inference engines (vLLM, Ollama, llama.cpp, TensorRT-LLM).

---

## Latency Decomposition Model

```mermaid
sequenceDiagram
    autonumber
    actor Client as Profiler Client
    participant Engine as LLM Inference Server

    Client->>Engine: Send Prompt Tokens (Pre-fill Request)
    Note over Engine: KV-Cache Allocation & Prompt Attention
    Engine-->>Client: Stream Chunk 1 (First Token)
    Note over Client,Engine: Time-To-First-Token (TTFT) Window

    loop Autoregressive Decoding Loop
        Engine-->>Client: Stream Chunk N (Token Delta)
        Note over Client: Measure Inter-Token Latency (ITL)
    end

    Note over Client: Compute P50, P90, P99 Percentiles & Tokens/Sec
```

---

## Key Metrics Profiled

- **Time-to-First-Token (TTFT):** Measures pre-fill processing time and time until first token emission.
- **Inter-Token Latency (ITL):** Measures consecutive token emission intervals throughout autoregressive generation.
- **Throughput ($tokens/sec$):** End-to-end token generation rate under target concurrency.
- **Percentile Distributions ($P_{50}, P_{90}, P_{95}, P_{99}$):** High-resolution tail-latency identification.
- **Terminal Visualization:** Real-time ASCII distribution histograms right in your console.

---

## Installation

```bash
git clone https://github.com/GuptaSoujanya/inference-latency-profiler.git
cd inference-latency-profiler
pip install -e .
```

---

## Quickstart

Run a fast profile benchmark:

```bash
python -m profiler.cli --model qwen-2.5-7b --requests 5 --tokens 32
```

Sample Output:
```text
========================================================
         INFERENCE LATENCY PROFILE REPORT
========================================================
 Total Requests Completed    : 5
 Total Tokens Sampled        : 160
 Overall Token Throughput    : 54.21 tokens/sec
--------------------------------------------------------
 Time-To-First-Token (TTFT)  : Mean = 64.12 ms
   P50: 63.80 ms | P90: 71.40 ms | P99: 74.20 ms
--------------------------------------------------------
 Inter-Token-Latency (ITL)   : Mean = 18.04 ms
   P50: 17.90 ms | P90: 21.30 ms | P99: 23.40 ms
--------------------------------------------------------
 Memory Footprint            : RSS = 42.4 MB | Peak VRAM = 3420.0 MB
========================================================

--- Inter-Token Latency Distribution ---
[  14.5 -   16.3 ms] | ##########                     (28)
[  16.3 -   18.1 ms] | ############################## (82)
[  18.1 -   19.9 ms] | #################              (45)
[  19.9 -   21.7 ms] | ##                             (5)
```

---

## Running Test Suite

```bash
python -m unittest discover tests -v
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
