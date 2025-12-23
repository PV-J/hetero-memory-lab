# examples/example_bandwidth_sweep.py

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from memory_lab.system_model import SystemModel
from memory_lab.compute_core import ComputeCore
from memory_lab.memory_model import MemoryModel

def run_bandwidth_sweep(access_pattern: str) -> None:
    print(f"\n=== Bandwidth sweep ({access_pattern}) ===")

    problem_size_mb = 10
    problem_size_bytes = problem_size_mb * 1024 * 1024
    ops_per_byte_low = 1.0   # low arithmetic intensity
    ops_per_byte_high = 32.0 # high arithmetic intensity

    # Define a compute core (unchanged)
    compute = ComputeCore(peak_flops=1e9)  # example: 1 GFLOP/s

    # Low vs high bandwidth scenarios
    for bandwidth_gbps in [1.0, 100.0]:
        mem = MemoryModel(
            bandwidth_gbps=bandwidth_gbps,
            base_latency_s=0.0,
            two_tier=False,
            access_pattern=access_pattern,  # NEW
        )

        system = SystemModel(memory=mem, compute=compute)

        for ops_per_byte in [ops_per_byte_low, ops_per_byte_high]:
            result = system.run_kernel(
                num_bytes=problem_size_bytes,
                ops_per_byte=ops_per_byte,
            )

            print("---")
            print(f"Bandwidth: {bandwidth_gbps} Gbit/s")
            print(f"Ops per byte: {ops_per_byte}")
            print(f"Memory time: {result.memory_time:.3e} s")
            print(f"Compute time: {result.compute_time:.3e} s")
            print(f"Total time: {result.total_time:.3e} s")
            print(f"Regime: {result.regime}")


if __name__ == "__main__":
    for pattern in ["sequential", "random"]:
        run_bandwidth_sweep(pattern)
