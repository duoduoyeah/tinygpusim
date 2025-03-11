from typing import List, Tuple
import numpy as np


class TextureAddressing:
    """
    Texture Addressing (TA) block handles memory coalescing for vector memory operations.

    Responsible for:
    1. Combining multiple memory accesses into fewer transactions
    2. Handling vectorized load/store instructions
    3. Optimizing memory bandwidth usage
    """

    def __init__(self, transaction_size: int = 64):
        """
        Args:
            transaction_size: Size of a single memory transaction in bytes (typically 64B)
        """
        self.transaction_size = transaction_size
        self.stats = {
            "total_requests": 0,
            "coalesced_transactions": 0,
            "total_transactions": 0,
        }

    def coalesce_memory_requests(
        self, addresses: List[int], sizes: List[int]
    ) -> List[Tuple[int, int]]:
        """
        Coalesce multiple memory requests into fewer transactions.

        Args:
            addresses: List of memory addresses to access
            sizes: List of sizes for each access

        Returns:
            List of (start_address, size) tuples representing coalesced transactions
        """
        if not addresses:
            return []

        self.stats["total_requests"] += len(addresses)

        # Sort addresses to find consecutive regions
        addr_size_pairs = sorted(zip(addresses, sizes))

        # Coalesce nearby addresses into single transactions
        coalesced = []
        current_start = addr_size_pairs[0][0]
        current_end = current_start + addr_size_pairs[0][1]

        for addr, size in addr_size_pairs[1:]:
            # If this address is within transaction_size of current region, extend it
            if addr <= current_end + self.transaction_size:
                current_end = max(current_end, addr + size)
            else:
                # Start new transaction
                coalesced.append((current_start, current_end - current_start))
                current_start = addr
                current_end = addr + size

        # Add final transaction
        coalesced.append((current_start, current_end - current_start))

        self.stats["coalesced_transactions"] += len(coalesced)
        self.stats["total_transactions"] += len(addresses)

        return coalesced

    def get_coalescing_stats(self):
        """Return memory coalescing statistics"""
        stats = self.stats.copy()
        if stats["total_transactions"] > 0:
            stats["coalescing_ratio"] = (
                stats["coalesced_transactions"] / stats["total_transactions"]
            )
        else:
            stats["coalescing_ratio"] = 1.0
        return stats
