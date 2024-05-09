import argparse
from .engine import LatencyProfiler

def main():
    parser = argparse.ArgumentParser(prog="llm-profile")
    parser.add_argument("--tokens", type=int, default=32)
    args = parser.parse_args()

    profiler = LatencyProfiler()
    res = profiler.profile_run(num_tokens=args.tokens)

    print("\n" + "="*52)
    print("         INFERENCE LATENCY PROFILE REPORT")
    print("="*52)
    print(f" Sampled Tokens Generated  : {res['tokens']}")
    print(f" Overall Token Throughput  : {res['throughput_tok_s']} tokens/sec")
    print(f" Time-To-First-Token (TTFT): {res['ttft_ms']} ms")
    print(f" Inter-Token-Latency (ITL) : Mean={res['itl_mean_ms']} ms | P50={res['itl_p50']} ms | P99={res['itl_p99']} ms")
    print("="*52 + "\n")

if __name__ == "__main__":
    main()
