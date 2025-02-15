class L1Cache:
    """32KB L1 data cache with LRU policy
    Args:
        line_size (int): Cache line size in bytes
        ways (int): Associativity
    Attributes:
        tags: Cache tag storage
        lru_counter: Replacement tracking
    """

    def __init__(self, line_size=64, ways=4):
        self.line_size = line_size
        self.ways = ways
        self.tags = {}
        self.lru_counter = 0

    def access(self, address, is_write):
        """Handle cache access
        Args:
            address (int): Memory address
            is_write (bool): Write operation flag
        Returns:
            bool: True if hit
        """
        tag = address // self.line_size
        set_idx = tag % self.ways

        if tag in self.tags.get(set_idx, []):
            # Hit
            self.lru_counter += 1
            return True
        # Miss handling
        return False
