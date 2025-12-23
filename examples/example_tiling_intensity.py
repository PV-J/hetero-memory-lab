# examples/example_tiling_intensity.py
"""
Demonstrate how loop tiling increases arithmetic intensity (ops/byte),
shifting workloads rightward on a roofline plot from memory-bound to balanced/compute-bound.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from memory_lab.system_model import SystemModel
from memory_lab.compute_core import ComputeCore
from memory_lab.memory_model import MemoryModel


def run_tiling_experiment(access_pattern: str, reuse_factor: float, label: str) -> None:
    """Run one case: naive vs tiled, same problem size and base ops/byte."""
    print(f"\n=== Tiling experiment ({access_pattern}, {label}) ===")
    
    # Fixed problem: 10MB matrix multiply style workload
    problem_size_mb = 10
    problem_size_bytes = problem_size_mb * 1024 * 1024
    
    # Base arithmetic intensity: naive matmul-style (2 loads + 1 store per multiply)
    base_ops_per_byte = 2.0  # FMA: 2 FLOPs per byte loaded
    
    # Tiled version gets REUSE_FACTOR times more ops per byte loaded
    tiled_ops_per_byte = base_ops_per_byte * reuse_factor
    
    # Fixed compute + memory system
    compute = ComputeCore(peak_flops=1e12)  # 1 TFLOP/s (realistic GPU)
    mem = MemoryModel(
        bandwidth_gbps=1000.0,  # 1 TB/s HBM
        base_latency_s=0.0,
        two_tier=False,
        access_pattern=access_pattern,
    )
    
    # FIXED: Use correct SystemModel constructor (matching example_bandwidth_sweep.py)
    print("Naive (no tiling):")
    naive_system = SystemModel(
        problem_size_bytes=problem_size_bytes,
        compute_core=compute,
        memory_model=mem,
    )
    naive_result = naive_system.run()
    print(f"  Ops/byte: {base_ops_per_byte:.1f}, Regime: {naive_result['regime']}")
    print(f"  Memory time: {naive_result['memory_time_s']:.3e}s, Compute time: {naive_result['compute_time_s']:.3e}s")
    
    print("Tiled:")
    tiled_system = SystemModel(
        problem_size_bytes=problem_size_bytes,
        compute_core=ComputeCore(peak_flops=1e12, ops_per_byte=tiled_ops_per_byte),  # Pass ops/byte here?
        memory_model=mem,
    )
    tiled_result = tiled_system.run()
    print(f"  Ops/byte: {tiled_ops_per_byte:.1f}, Regime: {tiled_result['regime']}")
    print(f"  Memory time: {tiled_result['memory_time_s']:.3e}s, Compute time: {tiled_result['compute_time_s']:.3e}s")


if __name__ == "__main__":
    # Case 1: sequential access, no reuse (naive)
    run_tiling_experiment("sequential", reuse_factor=1.0, label="no reuse")
    
    # Case 2: sequential access, 8x reuse (good tiling)
    run_tiling_experiment("sequential", reuse_factor=8.0, label="8x reuse")
    
    # Case 3: random access, even with tiling still struggles
    run_tiling_experiment("random", reuse_factor=8.0, label="8x reuse (random)")
