import argparse
from .config import ProfilerConfig
from .engine import LatencyProfiler
from .visualization import render_ascii_histogram
from .telemetry.memory import get_system_memory_snapshot

def main():
    parser = argparse.ArgumentParser(
        prog="llm-profile",
        description="inference-latency-profiler: High-precision TTFT & ITL latency analyzer."
    )
    parser.add_argument("--model", type=str, default="qwen-2.5-7b-instruct", help="Model identifier")
    parser.add_argument("--requests", type=int, default=5, help="Number of profiling requests")
    parser.add_argument("--tokens", type=int, default=32, help="Generated tokens per request")
    parser.add_argument("--backend", type=str, choices=["mock"], default="mock", help="Inference backend")

    args = parser.parse_args()

    cfg = ProfilerConfig(
        model_name=args.model,
        backend=args.backend,
        num_requests=args.requests,
        generate_tokens=args.tokens
    )

    print(f"\n[inference-latency-profiler] Profiling '{cfg.model_name}' ({cfg.num_requests} runs, {cfg.generate_tokens} tokens/req)...")
    profiler = LatencyProfiler(cfg)
    stats, records = profiler.run_benchmark()
    mem = get_system_memory_snapshot()

    print("\n" + "="*56)
    print("         INFERENCE LATENCY PROFILE REPORT")
    print("="*56)
    print(f" Total Requests Completed    : {stats.total_requests}")
    print(f" Total Tokens Sampled        : {stats.total_tokens_generated}")
    print(f" Overall Token Throughput    : {stats.mean_throughput:.2f} tokens/sec")
    print("-" * 56)
    print(f" Time-To-First-Token (TTFT)  : Mean = {stats.mean_ttft_ms:.2f} ms")
    print(f"   P50: {stats.ttft_percentiles['p50']} ms | P90: {stats.ttft_percentiles['p90']} ms | P99: {stats.ttft_percentiles['p99']} ms")
    print("-" * 56)
    print(f" Inter-Token-Latency (ITL)   : Mean = {stats.mean_itl_ms:.2f} ms")
    print(f"   P50: {stats.itl_percentiles['p50']} ms | P90: {stats.itl_percentiles['p90']} ms | P99: {stats.itl_percentiles['p99']} ms")
    print("-" * 56)
    print(f" Memory Footprint            : RSS = {mem.rss_mb:.1f} MB | Peak VRAM = {mem.simulated_vram_peak_mb:.1f} MB")
    print("="*56 + "\n")

    all_itl = []
    for r in records:
        all_itl.extend(r.inter_token_latencies_ms)
    print(render_ascii_histogram(all_itl, bins_count=5, title="Inter-Token Latency Distribution"))
    print()

if __name__ == "__main__":
    main()
