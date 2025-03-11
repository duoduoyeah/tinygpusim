from ..mem.dram import DRAMController
from tinygpusim.cpu.cpu_mem import CPUMemory
from typing import Optional
from ..computation_entities import Kernel


class DMAEngine:
    """Handles data transfers between memory and other components.
    Args:
        dram (DRAMController): Memory controller.
        num_channels (int): Number of DMA channels.

    Attributes:
        channels: Active DMA channels.
    """

    def __init__(
        self,
        id: int,
        dram: DRAMController,
        cpu: CPUMemory,
    ):
        """
        initializes the DMA engine.

        Input:
            dram (DRAMController): Memory controller.
            num_channels (int): Number of DMA channels.
        """
        self.id = id
        self.cpu: CPUMemory = cpu
        self.dram: DRAMController = dram
        self.kernel: Optional[Kernel] = None
        self._available = True

    @property
    def available(self) -> bool:
        return self._available

    def demand(self, kernel: Kernel):
        """Process a memory copy command from the command processor"""
        self.kernel = kernel
        self._available = False

        # Extract memory copy parameters from the kernel
        src_addr = kernel.src_addr
        dst_addr = kernel.dst_addr
        size = kernel.size

        # Perform the actual memory copy
        self.copy_from_cpu_to_dram(src_addr, dst_addr, size)

        # Mark as complete
        self.kernel = None
        self._available = True

    def receive_kernel(self, kernel: Kernel):
        """Receive a kernel from the CPU"""
        # For backward compatibility - redirect to demand
        self.demand(kernel)

    def update_available(self):
        """Update the availability of the DMA engine"""
        self._available = self.kernel is None

    def copy_from_cpu_to_dram(self, src_addr, dst_addr, size):
        """Copies data from CPU memory to DRAM."""
        data = self.cpu.read(src_addr, size)
        self.dram.write(dst_addr, data)


if __name__ == "__main__":
    pass
