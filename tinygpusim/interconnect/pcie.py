class PCIe:
    def __init__(self, speed: int = 16):
        self.speed = speed

    def transfer(
        self,
        data: bytes,
        dst_addr: int,
        size: int,
    ) -> None:
        """Simulates a data transfer over PCIe."""
        return data, dst_addr, size
