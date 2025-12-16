# examples/example_cache_sweep.py

from memory_lab.system_model import SystemModel
from memory_lab.memory_model import MemoryModel

def run_profile(name: str, hit_rate: float):
    mem = MemoryModel(
        base_latency=50e-9,
        fast_bandwidth_gbps=500.0,
        slow_bandwidth_gbps=10.0,
        hit_rate=hit_rate,
    )
    system = SystemModel(memory_model=mem)

    bytes_count = system.problem_size_bytes
    mem_time = mem.access_two_tier(bytes_count)
    comp_time = system.compute_core.compute_time_for_bytes(bytes_count)
    total_time = mem_time + comp_time
    regime = (
        "memory-bound" if mem_time > comp_time
        else "compute-bound" if comp_time > mem_time
        else "balanced"
    )

    print(f"=== {name} ===")
    print(f"Hit rate:     {hit_rate:.2f}")
    print(f"Fast BW:      {mem.fast_bandwidth_gbps} Gbit/s")
    print(f"Slow BW:      {mem.slow_bandwidth_gbps} Gbit/s")
    print(f"Memory time:  {mem_time:.3e} s")
    print(f"Compute time: {comp_time:.3e} s")
    print(f"Total time:   {total_time:.3e} s")
    print(f"Regime:       {regime}")
    print()

if __name__ == "__main__":
    run_profile("Poor locality", hit_rate=0.1)
    run_profile("Moderate locality", hit_rate=0.5)
    run_profile("Good locality", hit_rate=0.95)
