# memory_lab/system_model.py

from dataclasses import dataclass, field
from typing import Dict, Any

from .memory_model import MemoryModel
from .compute_core import ComputeCore


@dataclass
class SystemModel:
    """
    Simple system model combining a compute core and a memory model
    for a single streaming kernel.

    - problem_size_bytes: total data size to process
    """

    problem_size_bytes: int = 10_000_000   # 10 MB

    # Use default_factory for mutable defaults (instances)
    compute_core: ComputeCore = field(default_factory=ComputeCore)
    memory_model: MemoryModel = field(default_factory=MemoryModel)

    def run(self) -> Dict[str, Any]:
        """
        Run the model and return timing breakdown and classification.
        """
        mem_time = self.memory_model.access(self.problem_size_bytes)
        comp_time = self.compute_core.compute_time_for_bytes(self.problem_size_bytes)
        total_time = mem_time + comp_time  # no overlap in this toy model

        if mem_time > comp_time:
            regime = "memory-bound"
        elif comp_time > mem_time:
            regime = "compute-bound"
        else:
            regime = "balanced"

        return {
            "problem_size_bytes": self.problem_size_bytes,
            "memory_time_s": mem_time,
            "compute_time_s": comp_time,
            "total_time_s": total_time,
            "regime": regime,
        }
