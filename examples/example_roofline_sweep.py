# examples/example_roofline_sweep.py
"""
Generate roofline-style data: sweep arithmetic intensity (ops/byte) vs bandwidth
for sequential/random access patterns. Outputs CSV for external plotting.

Mimics real roofline tools: measures achieved FLOP/s vs arithmetic intensity.
"""

import os
import sys
import csv
from typing import List, Dict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from memory_lab.system_model import SystemModel
from memory_lab.compute_core import ComputeCore
from memory_lab.memory_model import MemoryModel


def generate_roofline_data(
    problem_size_bytes: int = 10 * 1024 * 1024,
    peak_flops: float = 19.5e12,  # A100 FP32: 19.5 TFLOP/s
    # problem_size_bytes: int = 10 * 1024 * 1024,
    # peak_flops: float = 2e12,  # 2 TFLOP/s (realistic mid-range GPU)
    # problem_size_bytes: int = 10 * 1024 * 1024,
    # peak_flops: float = 1e12,  # 1 TFLOP/s
) -> List[Dict[str, float]]:
    # bandwidths_gbps = [100.0, 500.0, 2000.0]  # Match HBM2: ~2 TB/s
    """Sweep ops/byte and bandwidth, return list of measurement points."""
    points = []
    
    # Sweep arithmetic intensity (ops/byte) - log scale
    ops_per_bytes = [0.1, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
    
    # Sweep bandwidth scenarios
    bandwidths_gbps = [100.0, 500.0, 1000.0]  # 100GB/s, 500GB/s, 1TB/s
    
    for access_pattern in ["sequential", "random"]:
        for bw_gbps in bandwidths_gbps:
            mem = MemoryModel(
                bandwidth_gbps=bw_gbps,
                base_latency_s=0.0,
                two_tier=False,
                access_pattern=access_pattern,
            )
            
            for ops_per_byte in ops_per_bytes:
                system = SystemModel(
                    problem_size_bytes=problem_size_bytes,
                    compute_core=ComputeCore(peak_flops=peak_flops),
                    memory_model=mem,
                )
                
                result = system.run()
                
                # Compute achieved performance metrics (what roofline tools measure)
                total_ops = problem_size_bytes * ops_per_byte
                achieved_flops = total_ops / result['total_time_s']  # FLOP/s achieved
                
                # Roofline X-axis: arithmetic intensity
                arithmetic_intensity = ops_per_byte  # ops/byte
                
                points.append({
                    'access_pattern': access_pattern,
                    'bandwidth_gbps': bw_gbps,
                    'ops_per_byte': ops_per_byte,
                    'achieved_flops': achieved_flops,
                    'arithmetic_intensity': arithmetic_intensity,
                    'memory_time_s': result['memory_time_s'],
                    'compute_time_s': result['compute_time_s'],
                    'regime': result['regime'],
                })
    
    return points


def save_roofline_csv(points: List[Dict[str, float]], filename: str = "roofline_data.csv"):
    """Save data to CSV for plotting in Excel/Matplotlib/etc."""
    if points:
        fieldnames = points[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(points)
        print(f"✓ Saved {len(points)} points to {filename}")
    else:
        print("No data to save")


if __name__ == "__main__":
    print("Generating roofline data...")
    
    # Generate the sweep
    points = generate_roofline_data()
    
    # Print summary table
    print("\n=== Roofline Summary Table ===")
    print(f"{'Pattern':<12} {'BW (GB/s)':<10} {'Ops/byte':<8} {'Achieved TFLOP/s':<12} {'Regime':<10}")
    print("-" * 60)
    
    for point in points[:12]:  # First 12 for preview
        bw_gb_s = point['bandwidth_gbps'] / 8  # Convert Gbit/s -> GB/s
        flops_tflop_s = point['achieved_flops'] / 1e12
        print(f"{point['access_pattern']:<12} {bw_gb_s:<10.0f} {point['ops_per_byte']:<8.1f} "
              f"{flops_tflop_s:<12.2f} {point['regime']:<10}")
    
    # Save full dataset
    save_roofline_csv(points)
    
    print("\n✅ Step 3 complete! Use roofline_data.csv with any plotting tool.")
    print("Real tools (Intel Advisor, Kerncraft) use exactly this format: achieved FLOP/s vs arithmetic intensity [web:19][web:51]")
