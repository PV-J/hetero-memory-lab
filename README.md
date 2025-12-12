# hetero-memory-lab

`hetero-memory-lab` is a Python toy lab for exploring **memory bandwidth** and **compute‑ vs memory‑bound workloads**.

It models a simple streaming kernel that:

- Reads data from main memory with finite bandwidth.
- Performs a configurable number of operations per byte (arithmetic intensity).
- Reports separate **memory time**, **compute time**, and a **regime** classification:
  - `memory-bound` (memory dominates total time)
  - `compute-bound` (compute dominates)
  - `balanced`

The goal is to build intuition similar to the **roofline model**: how bandwidth and arithmetic intensity interact to determine whether a workload is limited by compute or by memory traffic. [web:395][web:401]

## Repository structure

- `memory_lab/`
  - `memory_model.py` – Main memory model with base latency and bandwidth.
  - `compute_core.py` – Compute core model with peak FLOP/s and ops per byte.
  - `system_model.py` – Combines compute + memory to classify regimes.
- `examples/`
  - `example_bandwidth_sweep.py` – Sweeps bandwidth and arithmetic intensity, prints timing and regime.
- `tests/` – (optional, to be added later)

## Quickstart

Clone the repo and run the example sweep:

'''bash
git clone https://github.com/<your-user>/hetero-memory-lab.git
cd hetero-memory-lab

python examples/example_bandwidth_sweep.py
'''

You should see output similar to:

'''bash
=== Low bandwidth ===
Problem size: 10 MB
Bandwidth: 1.0 Gbit/s
Ops per byte: 1.0
Memory time: 8.388613e-02 s
Compute time: 1.048576e-03 s
Total time: 8.493471e-02 s
Regime: memory-bound

=== High bandwidth ===
Problem size: 10 MB
Bandwidth: 100.0 Gbit/s
Ops per byte: 1.0
Memory time: 8.389108e-04 s
Compute time: 1.048576e-03 s
Total time: 1.887487e-03 s
Regime: compute-bound

=== Low arithmetic intensity ===
...
Regime: memory-bound

=== High arithmetic intensity ===
...
Regime: compute-bound
'''

This demonstrates:

- With **low bandwidth**, the workload is memory‑bound.
- With **high bandwidth**, the same workload becomes compute‑bound.
- At fixed bandwidth, **low arithmetic intensity** is memory‑bound, while **high arithmetic intensity** is compute‑bound.

## Next steps

Planned enhancements:

- [X] Add a simple cache model (hit/miss, effective bandwidth).
- [X] Add an `access_pattern` parameter (sequential vs random).
- [X] Add example scripts for “tiling” and locality experiments.
- [X] Document how this toy model relates to real accelerator memory systems.
