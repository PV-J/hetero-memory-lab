# hetero-memory-lab

## 🔍 Findable By

**Google:** roofline model tutorial, gpu memory bound, arithmetic intensity matrix multiply, tiling cache optimization  
**GitHub:** roofline-model gpu-performance memory-bandwidth hpc cuda intel-advisor kerncraft  
**Medium:** Roofline Model GPU Performance High Performance Computing Memory Bandwidth

`hetero-memory-lab` is a Python toy lab for exploring **memory bandwidth** and **compute‑ vs memory‑bound workloads**.

It models a simple streaming kernel that:

- Reads data from main memory with finite bandwidth.
- Performs a configurable number of operations per byte (arithmetic intensity).
- Reports separate **memory time**, **compute time**, and a **regime** classification:
  - `memory-bound` (memory dominates total time)
  - `compute-bound` (compute dominates)
  - `balanced`

The goal is to build intuition similar to the **roofline model**: how bandwidth and arithmetic intensity interact to determine whether a workload is limited by compute or by memory traffic. 

## Repository structure

- `memory_lab/`
  - `memory_model.py` – Main memory model with base latency, bandwidth, and an optional two-tier (fast + slow) mode.
  - `compute_core.py` – Compute core model with peak FLOP/s and ops per byte.
  - `system_model.py` – Combines compute + memory to classify regimes.
- `examples/`
  - `example_bandwidth_sweep.py` – Sweeps bandwidth and arithmetic intensity, prints timing and regime.
  - `example_cache_sweep.py` – Sweeps hit rate in a two-tier memory model (poor vs good locality).

## Quickstart

Clone the repo and run the example sweep:

```bash
git clone https://github.com/<PV-J>/hetero-memory-lab.git
cd hetero-memory-lab

python examples/example_bandwidth_sweep.py
```
You should see output similar to:

```
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
```

This demonstrates:

- With **low bandwidth**, the workload is memory‑bound.
- With **high bandwidth**, the same workload becomes compute‑bound.
- At fixed bandwidth, **low arithmetic intensity** is memory‑bound, while **high arithmetic intensity** is compute‑bound.

To try the two-tier cache-style model:
```bash
python -m examples.example_cache_sweep
```

You should see “Poor locality,” “Moderate locality,” and “Good locality” cases with different hit rates, memory times, and regime labels.

You should see output similar to:
```
=== Poor locality ===
Hit rate: 0.10
Fast BW: 500.0 Gbit/s
Slow BW: 10.0 Gbit/s
Memory time: 7.216e-03 s
Compute time: 1.000e-03 s
Total time: 8.216e-03 s
Regime: memory-bound

=== Moderate locality ===
Hit rate: 0.50
Fast BW: 500.0 Gbit/s
Slow BW: 10.0 Gbit/s
Memory time: 4.080e-03 s
Compute time: 1.000e-03 s
Total time: 5.080e-03 s
Regime: memory-bound

=== Good locality ===
Hit rate: 0.95
Fast BW: 500.0 Gbit/s
Slow BW: 10.0 Gbit/s
Memory time: 5.521e-04 s
Compute time: 1.000e-03 s
Total time: 1.552e-03 s
Regime: compute-bound
```
Above results show locality shifting you from memory‑bound to compute‑bound within the same basic setup.

```
- Poor locality → memory time ≫ compute time → memory‑bound.

- Good locality → memory time < compute time → compute‑bound.
```
For above results, increased fast‑tier bandwidth and hit rate to simulate a well‑tiled, cache‑friendly kernel.

## Next steps

Planned enhancements:

- [X] Add a simple cache-style two-tier memory model (hit rate, effective bandwidth).
- [X] Add an `access_pattern` parameter (sequential vs random).
- [X] Add example scripts for tiling and locality experiments.
- [X] Document how this toy model relates to real accelerator memory systems and roofline tools.

## Roadmap

This lab is designed to grow over a small series of posts. Planned enhancements include:

- Cache model
  - Add a simple `CacheModel` with hit rate and effective bandwidth.
  - Show how changing hit rate shifts the memory time and regime.

- Access patterns
  - Introduce an `access_pattern` parameter (sequential vs random).
  - Let users see how poor locality reduces effective bandwidth.

- Tiling and arithmetic intensity
  - Add an example that “tiles” the work to increase arithmetic intensity.

- Profiling connections
  - Add notes on mapping lab parameters to real CPU/GPU specs.
  - Link the toy model to roofline charts from vendor tools.
