from .direct_mem_access import DMAEngine
from .async_compute_engine import AsyncComputeEngine
from tinygpusim.cpu.command_generator import Command


class CommandProcessor:
    """Handles commands from the CPU for GPU processing
    This class receives commands such as memory-copying and kernel-launching
    from the CPU and delegates them to appropriate GPU blocks.

    Attributes:
        dma_engine: DMA engine for memory transfers
        async_compute_engine: Async compute engine for kernel execution
    """

    def __init__(self, dma_engine: DMAEngine, async_compute_engine: AsyncComputeEngine):
        self.dma_engine: DMAEngine = dma_engine
        self.async_compute_engine: AsyncComputeEngine = async_compute_engine

    def process_command(self, command: Command):
        """Process a command received from the CPU
        Args:
            command (Command): Command details including type and parameters
        Returns:
            bool: True if command processed successfully
        Raises:
            ValueError: If command type is unknown
        """
        command_type = command.type
        if command_type == "memory_copy":
            # Forward to DMA engine
            return self.dma_engine.handle_memory_copy(command)
        elif command_type == "kernel_launch":
            # Forward to ACE units
            return self.async_compute_engine.launch_kernel(command)
        else:
            raise ValueError("Unknown command type")
