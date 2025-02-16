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
