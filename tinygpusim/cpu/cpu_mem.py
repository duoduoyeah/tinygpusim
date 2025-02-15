class CPUMemory:
    """
    Represents the CPU memory.

    This class simulates the CPU memory and provides methods to read and write data.
    """

    def __init__(self, size):
        """
        Initializes the CPU memory with a given size.
        """
        self.size = size
        self.memory = bytearray(size)

    def read(self, address, size):
        """
        Reads data from the CPU memory.
        """
        if address < 0 or address + size > self.size:
            raise IndexError("Invalid memory access")
        return self.memory[address:address + size]

    def write(self, address, data):
        """
        Writes data to the CPU memory.
        """
        if address < 0 or address + len(data) > self.size:
            raise IndexError("Invalid memory access")
        self.memory[address:address + len(data)] = data
