import os
import resource
from dataclasses import dataclass

@dataclass
class MemorySnapshot:
    rss_mb: float
    simulated_vram_used_mb: float
    simulated_vram_peak_mb: float

def get_system_memory_snapshot() -> MemorySnapshot:
    """Capture current process RSS memory and simulated GPU VRAM allocation."""
    # maxrss in Darwin is in bytes, in Linux is in kilobytes
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_mb = usage / (1024 * 1024) if sys_is_darwin() else usage / 1024.0
    return MemorySnapshot(
        rss_mb=round(rss_mb, 2),
        simulated_vram_used_mb=2150.0,
        simulated_vram_peak_mb=3420.0
    )

def sys_is_darwin() -> bool:
    import platform
    return platform.system() == "Darwin"
