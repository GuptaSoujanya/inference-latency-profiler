import math
from typing import List, Dict

def calculate_percentiles(values: List[float], percentiles=[50, 90, 95, 99]) -> Dict[str, float]:
    if not values: return {f"p{p}": 0.0 for p in percentiles}
    sorted_v = sorted(values)
    n = len(sorted_v)
    res = {}
    for p in percentiles:
        idx = min(int((n - 1) * (p / 100.0)), n - 1)
        res[f"p{p}"] = round(sorted_v[idx], 3)
    return res
