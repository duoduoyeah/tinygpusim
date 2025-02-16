from typing import List, Optional
from dataclasses import field
from ..computation_entities import Workgroup, Wavefront
from .local_data_share import LocalDataShare


class ComputeUnit:
    """SIMD processing unit with register file
    Args:
        simd_width (int): Number of parallel ALUs
    Attributes:
        reg_file: Vector register storage
        cycle_count: Total executed cycles
    """

    def __init__(self, local_data_share: LocalDataShare):
        self.waverfront_slots = field(default_factory=list)
        self.scalar_registers = field(default_factory=list)
        self.vector_registers = field(default_factory=list)
        self.local_data_share = local_data_share


class ShaderArray:
    """Array of compute units in a shader engine
    Args:
        cu_count (int): Number of compute units in this array
    Attributes:
        compute_units: Ordered collection of compute units (List for sequential access)
    """

    def __init__(self, cu_count=4):
        data_share = LocalDataShare()
        self.compute_units: List[ComputeUnit] = [
            ComputeUnit(local_data_share=data_share) for _ in range(cu_count)
        ]


class ShaderEngine:
    """Main shader processing unit
    Args:
        pipe_depth (int): Maximum in-flight instructions
    Attributes:
        input_pipe: Input pipeline for shader instructions
    """

    def __init__(
        self,
        shader_arrays: List[ShaderArray],
    ):
        self.shader_arrays: List[ShaderArray] = shader_arrays


class ShaderPipeInput:
    """Front-end for shader instruction processing"""

    def __init__(self, shader_engine: ShaderEngine):
        self.shader_engine = shader_engine
        self.workgroup: Optional[Workgroup] = None

    def get_workgroup(self) -> Optional[Workgroup]:
        return self.workgroup

    def break_workgroup_into_wavefronts(self):
        """Break the workgroup into wavefronts"""
        wavefront_per_workgroup = 4
        if self.workgroup is not None:
            self.wavefronts = [
                Wavefront(self.workgroup) for _ in range(wavefront_per_workgroup)
            ]
