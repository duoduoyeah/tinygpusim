from typing import List
from .texture_addressing import TextureAddressing

class L1Cache:
    """32KB L1 data cache with LRU policy"""

    def __init__(self):
        pass


class L1VCache(L1Cache):
    """L1 Vector Cache with memory coalescing support"""

    def __init__(self, size=32 * 1024, line_size=64):
        super().__init__()
        self.size = size
        self.line_size = line_size
        self.texture_addressing = TextureAddressing(transaction_size=line_size)

    def vector_load(self, addresses: List[int], sizes: List[int]) -> List[bytes]:
        """
        Handle vectorized load operation with memory coalescing

        Args:
            addresses: List of addresses to load from
            sizes: Size of each load

        Returns:
            List of data loaded from each address
        """
        # Use TA block to coalesce requests
        coalesced_requests = self.texture_addressing.coalesce_memory_requests(
            addresses, sizes
        )

        # Perform coalesced memory transactions
        results = []
        for start_addr, size in coalesced_requests:
            data = self._load_block(start_addr, size)
            # Split coalesced data back into individual results
            results.extend(self._decoalesce_data(data, addresses, sizes))

        return results


class L1SCache(L1Cache):
    """L1 Scalar Cache."""

    def __init__(self):
        super().__init__()
        pass


class L1ICache(L1Cache):
    """L1 Instruction Cache."""

    def __init__(self):
        super().__init__()
        pass
