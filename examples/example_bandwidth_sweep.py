# examples/example_bandwidth_sweep.py

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from memory_lab.system_model import SystemModel
from memory_lab.compute_core import ComputeCore
from memory_lab.memory_model import MemoryModel


def run_case(problem_size_mb, bandwidth_gbps, ops_per_byte, label):
    bytes_total = int(problem_size_mb * 1024 * 1024)

    system = SystemModel(
        problem_size_bytes=bytes_total,
        compute_core=ComputeCore(peak_flops=10e9, ops_per_byte=ops_per_byte),
        memory_model=MemoryModel(base_latency=50e-9, bandwidth_gbps=bandwidth_gbps),
    )

    result = system.run()

    print(f"\n=== {label} ===")
    print(f"Problem size: {problem_size_mb} MB")
    print(f"Bandwidth: {bandwidth_gbps} Gbit/s")
    print(f"Ops per byte: {ops_per_byte}")
    print(f"Memory time:  {result['memory_time_s']:.6e} s")
    print(f"Compute time: {result['compute_time_s']:.6e} s")
    print(f"Total time:   {result['total_time_s']:.6e} s")
    print(f"Regime:       {result['regime']}")


def main():
    # Same problem & compute, different bandwidths
    run_case(problem_size_mb=10, bandwidth_gbps=1.0, ops_per_byte=1.0, label="Low bandwidth")
    run_case(problem_size_mb=10, bandwidth_gbps=10.0, ops_per_byte=1.0, label="Moderate bandwidth")
    run_case(problem_size_mb=10, bandwidth_gbps=100.0, ops_per_byte=1.0, label="High bandwidth")

    # Same bandwidth, varying arithmetic intensity
    run_case(problem_size_mb=10, bandwidth_gbps=10.0, ops_per_byte=0.1, label="Low arithmetic intensity")
    run_case(problem_size_mb=10, bandwidth_gbps=10.0, ops_per_byte=10.0, label="High arithmetic intensity")


if __name__ == "__main__":
    main()
