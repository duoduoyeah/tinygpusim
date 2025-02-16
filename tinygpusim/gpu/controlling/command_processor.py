from .direct_mem_access import DMAEngine
from .async_compute_engine import AsyncComputeEngine
from ..computation_entities import Kernel
from typing import List

from collections import deque


class CommandProcessor:
    """Handles commands from the CPU for GPU processing
    This class receives commands such as memory-copying and kernel-launching
    from the CPU and delegates them to appropriate GPU blocks.

    
    Attributes:
        dma_engine: DMA engine for memory transfers
        async_compute_engine: Async compute engine for kernel execution
        available_dma: Queue of available DMA engines
        available_ace: Queue of available ACE units
        command_queue: Queue of commands to be processed
    """

    def __init__(
        self,
        dma_engines: List[DMAEngine],
        async_compute_engines: List[AsyncComputeEngine],
    ):
        self.dma_engines = {
            dma_engine.id: dma_engine for dma_engine in dma_engines
        }

        self.async_compute_engines = {
            async_compute_engine.id: async_compute_engine
            for async_compute_engine in async_compute_engines
        }

        self.available_dma: deque[int] = deque(
            dma_engine.id for dma_engine in dma_engines)
        self.available_ace: deque[int] = deque(
            async_compute_engine.id for async_compute_engine in async_compute_engines
        )

        self.command_queue: List[Kernel] = []

    def enqueue_command(self, kernel: Kernel):
        self.command_queue.append(kernel)

    def find_available_dma(self) -> int:
        return self.available_dma.popleft()

    def find_available_ace(self) -> int:
        return self.available_ace.popleft()

    def add_available_dma(self):
        for dma_engine in self.dma_engines.values():
            if dma_engine.available:
                self.available_dma.append(dma_engine.id)

    def add_available_ace(self):
        for async_compute_engine in self.async_compute_engines.values():
            if async_compute_engine.available:
                self.available_ace.append(async_compute_engine.id)

    def process_command(self, kernel: Kernel):
        """Process a command received from the CPU
        Args:
            command (Command): Command details including type and parameters
        Returns:
            bool: True if command processed successfully
        Raises:
            ValueError: If command type is unknown
        """
        command_type = kernel.type
        if command_type == "memory_copy":
            dma_engine_id = self.find_available_dma()
            self.demand_to_dma_engine(kernel, dma_engine_id)
        elif command_type == "kernel_launch":
            ace_engine_id = self.find_available_ace()
            self.demand_to_async_compute_engine(kernel, ace_engine_id)
        else:
            raise ValueError("Unknown command type")

    def demand_to_dma_engine(self, kernel: Kernel, dma_engine_id: int):
        """Demand to a DMA engine"""
        self.dma_engines[dma_engine_id].demand(kernel)

    def demand_to_async_compute_engine(self, kernel: Kernel, ace_engine_id: int):
        """Demand to an ACE unit"""
        self.async_compute_engines[ace_engine_id].receive_kernel(kernel)
