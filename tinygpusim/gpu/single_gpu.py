from typing import List

from .controlling import DMAEngine, AsyncComputeEngine, CommandProcessor
from .mem.dram import DRAMController
from ..cpu.single_cpu import CPU


class GPU:
    def __init__(
        self,
        dram: DRAMController,
        cpu: CPU,
        dma_engine_nums: int = 2,
        ace_nums: int = 16,
    ):
        self.dma_engines: List[DMAEngine] = [
            DMAEngine(id=i, dram=dram, cpu=cpu) for i in range(dma_engine_nums)
        ]
        self.async_compute_engines: List[AsyncComputeEngine] = [
            AsyncComputeEngine(id=i) for i in range(ace_nums)
        ]
        self.command_processor = CommandProcessor(
            self.dma_engines, self.async_compute_engines
        )
        self.cpu = cpu
