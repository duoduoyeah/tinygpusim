from ..mem.dram import DRAMController
from tinygpusim.cpu.cpu_mem import CPUMemory
class DMAEngine:
    """Handles data transfers between memory and other components.

    The DMA engine fetches small chunks from the CPU's system memory
    and directly stores them in its local DRAM.

    A GPU-to-CPU memory copy follows a similar pattern in the opposite direction.

    A DMA engine oversees the memory transfer but cannot handle two memory
    copying commands simultaneously.

    Most GPUs are equipped with two DMA engines, such that two memory copies can
    be processed concurrently in the same or opposite directions.

    Args:
        dram (DRAMController): Memory controller.
        num_channels (int): Number of DMA channels.

    Attributes:
        channels: Active DMA channels.
    """

    def __init__(self, dram: DRAMController, cpu: CPUMemory):
        """
        initializes the DMA engine.

        Input:
            dram (DRAMController): Memory controller.
            num_channels (int): Number of DMA channels.
        """
        self.cpu: CPUMemory = cpu
        self.dram: DRAMController = dram

    def copy_from_cpu_to_dram(self, src_addr, dst_addr, size):
        """Copies data from CPU memory to DRAM.

        Args:
            src_addr (int): Source address in CPU memory.
            dst_addr (int): Destination address in DRAM.
            size (int): Number of bytes to copy.
        """
        data = self.cpu.read(src_addr, size)
        self.dram.write(dst_addr, data)


if __name__ == "__main__":
    pass