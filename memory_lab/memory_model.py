# memory_lab/memory_model.py

from dataclasses import dataclass


@dataclass
class MemoryModel:
    """
    Toy main memory model with:
      - base_latency: fixed cost per access (e.g., DRAM access latency)
      - bandwidth_gbps: sustained bandwidth in gigabits per second

    Latency model:
      total_latency = base_latency + (bytes * 8) / (bandwidth_gbps * 1e9)
    """

    base_latency: float = 50e-9        # 50 ns base latency
    bandwidth_gbps: float = 10.0       # 10 Gbit/s (approx 1.25 GB/s)

    def access(self, num_bytes: int) -> float:
        """
        Return latency (seconds) for transferring num_bytes.
        """
        if num_bytes <= 0:
            return 0.0

        bits = num_bytes * 8
        serialization_time = bits / (self.bandwidth_gbps * 1e9)
        return self.base_latency + serialization_time
