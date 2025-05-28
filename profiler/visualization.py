from typing import List

def render_ascii_histogram(values: List[float], bins_count: int = 6, title: str = "Latency Distribution (ms)") -> str:
    """Render a clean terminal-friendly text histogram for latency samples."""
    if not values:
        return "No data to render."
    min_v, max_v = min(values), max(values)
    if min_v == max_v:
        return f"{title}: All values at {min_v:.2f} ms"

    bin_width = (max_v - min_v) / bins_count
    bins = [0] * bins_count

    for v in values:
        idx = min(int((v - min_v) / bin_width), bins_count - 1)
        bins[idx] += 1

    max_count = max(bins) if max(bins) > 0 else 1
    bar_max_len = 30

    lines = [f"--- {title} ---"]
    for i in range(bins_count):
        b_start = min_v + i * bin_width
        b_end = b_start + bin_width
        count = bins[i]
        bar_len = int((count / max_count) * bar_max_len)
        bar = "#" * bar_len
        lines.append(f"[{b_start:6.1f} - {b_end:6.1f} ms] | {bar.ljust(bar_max_len)} ({count})")
    return "\n".join(lines)
