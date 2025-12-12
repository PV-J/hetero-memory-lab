# memory_lab/compute_core.py

from dataclasses import dataclass


@dataclass
class ComputeCore:
    """
    Toy compute core model.

    - peak_flops: peak floating point ops per second (FLOP/s)
    - ops_per_byte: how many operations are performed per byte loaded (arithmetic intensity)

    Compute time for N bytes:
      bytes -> ops = bytes * ops_per_byte
      compute_time = ops / peak_flops
    """

    peak_flops: float = 10e9      # 10 GFLOP/s
    ops_per_byte: float = 1.0     # arithmetic intensity

    def compute_time_for_bytes(self, num_bytes: int) -> float:
        """
        Return compute time (seconds) for processing num_bytes of data.
        """
        if num_bytes <= 0 or self.ops_per_byte <= 0 or self.peak_flops <= 0:
            return 0.0

        ops = num_bytes * self.ops_per_byte
        return ops / self.peak_flops
