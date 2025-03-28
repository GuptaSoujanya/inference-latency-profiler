import math
from typing import List, Dict

def calculate_percentiles(values: List[float], percentiles: List[int] = [50, 90, 95, 99]) -> Dict[str, float]:
    """Compute requested percentiles for a list of floating point values."""
    if not values:
        return {f"p{p}": 0.0 for p in percentiles}
    sorted_v = sorted(values)
    n = len(sorted_v)
    result = {}
    for p in percentiles:
        k = (n - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            val = sorted_v[int(k)]
        else:
            val = sorted_v[f] * (c - k) + sorted_v[c] * (k - f)
        result[f"p{p}"] = round(val, 3)
    return result
