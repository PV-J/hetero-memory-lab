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

    base_latency_s: float = 50e-9        # 50 ns base latency
    bandwidth_gbps: float = 10.0     # 10 Gbit/s (approx 1.25 GB/s)

    # NEW two-tier parameters for Part 2 (optional)
    two_tier: bool = False         # existing field
    fast_bandwidth_gbps: float = 0.0
    slow_bandwidth_gbps: float = 0.0
    hit_rate: float = 0.0  # 1.0 = all hits in fast tier

    # NEW: access pattern flag
    access_pattern: str = "sequential"  # "sequential" or "random"

    # You can also add a tunable penalty if you want:
    random_bw_factor: float = 0.25      # effective BW multiplier for random

    def _effective_bandwidth_gbps_single_tier(self) -> float:
        """Return effective bandwidth given access_pattern for single-tier model."""
        if self.access_pattern == "sequential":
            return self.bandwidth_gbps
        elif self.access_pattern == "random":
            # Random accesses waste cache lines and defeat prefetchers, so
            # effective bandwidth is reduced [web:80][web:82].
            return self.bandwidth_gbps * self.random_bw_factor
        else:
            raise ValueError(f"Unknown access_pattern: {self.access_pattern}")

    def _effective_bandwidth_gbps_two_tier(self) -> float:
        """
        Existing logic: combine fast/slow tiers via hit_rate to get an
        effective bandwidth. Then apply access_pattern penalty on top.
        """
        # Harmonic-mean style combination: 1 / Beff = h/Bfast + (1-h)/Bslow
        h = self.hit_rate
        b_fast = self.fast_bandwidth_gbps
        b_slow = self.slow_bandwidth_gbps
        beff = 1.0 / (h / b_fast + (1.0 - h) / b_slow)

        # Apply pattern penalty to the effective result.
        if self.access_pattern == "sequential":
            return beff
        elif self.access_pattern == "random":
            return beff * self.random_bw_factor
        else:
            raise ValueError(f"Unknown access_pattern: {self.access_pattern}")

    def effective_bandwidth_gbps(self) -> float:
        """
        Public helper: get effective bandwidth given tiering + access_pattern.
        """
        if self.two_tier:
            return self._effective_bandwidth_gbps_two_tier()
        else:
            return self._effective_bandwidth_gbps_single_tier()

    def time_for_bytes(self, num_bytes: float) -> float:
        """
        Compute memory time using effective bandwidth and base_latency.
        """
        bw = self.effective_bandwidth_gbps()
        # Convert Gbit/s to bytes/s: 1 Gbit/s = 1e9 / 8 bytes/s
        bytes_per_second = (bw * 1e9) / 8.0
        transfer_time = num_bytes / bytes_per_second
        return self.base_latency_s + transfer_time

    def access(self, num_bytes: int) -> float:
        """
        Return latency (seconds) for transferring num_bytes.
        """
        if num_bytes <= 0:
            return 0.0
        return self.time_for_bytes(num_bytes)   
        # bits = num_bytes * 8
        # serialization_time = bits / (self.bandwidth_gbps * 1e9)
        # return self.base_latency + serialization_time
    def access_two_tier(self, num_bytes: int) -> float:
        """
        Return latency (seconds) for transferring num_bytes
        using a simple two-tier model (fast + slow).

        The hit_rate fraction of traffic uses fast_bandwidth_gbps,
        the rest uses slow_bandwidth_gbps.
        """
        if num_bytes <= 0:
            return 0.0
        return self.time_for_bytes(num_bytes)
        
        #assert self.fast_bandwidth_gbps is not None
        #assert self.slow_bandwidth_gbps is not None

        #bits = num_bytes * 8
        #fast_bits = bits * self.hit_rate
        #slow_bits = bits * (1.0 - self.hit_rate)

        #fast_time = fast_bits / (self.fast_bandwidth_gbps * 1e9)
        #slow_time = slow_bits / (self.slow_bandwidth_gbps * 1e9)

        #return self.base_latency + fast_time + slow_time
    
