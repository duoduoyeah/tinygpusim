from typing import List


class DRAMController:
    """
    capacity in bytes
    """

    def __init__(self, capacity=8 * 1024**3):
        """
        Initializes the DRAM controller.

        Input:
            capacity (int): The capacity of the DRAM in bytes. Defaults to 8GB.
        Output:
            None
        Data structure changed:
            self.capacity (int): The capacity of the DRAM.
            self.storage (bytearray): The DRAM storage.
        Error:
            None
        """
        self.capacity = capacity
        self.storage: bytearray = bytearray(capacity)
        self.address_limit = capacity - 1

    def check_address(func):
        def wrapper(self, address, *args, **kwargs):
            if not 0 <= address <= self.address_limit:
                raise ValueError(
                    f"Address {address} out of range (0-{self.address_limit})"
                )
            return func(self, address, *args, **kwargs)

        return wrapper

    @check_address
    def load(self, address, size):
        """Read from memory"""
        return self.storage[address : address + size]

    @check_address
    def store(self, address, data):
        """Write to memory"""
        self.storage[address : address + len(data)] = data

    def vector_load(self, addresses: List[int], sizes: List[int]) -> List[bytes]:
        """
        Perform vectorized load operation

        Args:
            addresses: List of addresses to load from
            sizes: Size of each load

        Returns:
            List of data loaded from each address
        """
        results = []
        for addr, size in zip(addresses, sizes):
            results.append(self.load(addr, size))
        return results

    def vector_store(self, addresses: List[int], data: List[bytes]):
        """
        Perform vectorized store operation

        Args:
            addresses: List of addresses to store to
            data: List of data to store at each address
        """
        for addr, d in zip(addresses, data):
            self.store(addr, d)


if __name__ == "__main__":
    # Example usage
    dram = DRAMController(capacity=1024)  # 1KB DRAM
    address = 2048  # Out of range address
    data = b"Hello, DRAM!"
    try:
        dram.store(address, data)
        loaded_data = dram.load(address, len(data))
        print(f"Stored data: {data}")
        print(f"Loaded data: {loaded_data}")
    except ValueError as e:
        print(f"Error: {e}")
