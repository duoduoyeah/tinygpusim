class L2TLB:
    """
    L2 Translation Lookaside Buffer (L2TLB) in GPU is responsible for:
    1. Handling L1TLB misses
    2. Caching page table entries
    3. Communicating with memory management unit for page walks
    4. Providing virtual-to-physical address translations
    """

    def __init__(self, mmu, size=4096, page_size=4096):
        """
        Initialize the L2TLB.

        Args:
            mmu: Memory Management Unit that handles page walks on TLB misses
            size: Number of entries in the L2TLB
            page_size: Size of memory pages in bytes
        """
        self.mmu = mmu
        self.size = size
        self.page_size = page_size
        self.entries = {}  # Maps virtual page numbers to physical page numbers
        self.access_count = 0
        self.hit_count = 0
        self.miss_count = 0

    def lookup(self, virtual_address):
        """
        Look up a virtual address in the L2TLB.

        Args:
            virtual_address: The virtual address to translate

        Returns:
            tuple: (physical_address, hit_status)
                physical_address: Translated physical address or None if miss
                hit_status: True if L2TLB hit, False if miss
        """
        self.access_count += 1

        # Calculate virtual page number
        vpn = virtual_address // self.page_size

        # Calculate page offset
        offset = virtual_address % self.page_size

        if vpn in self.entries:
            # L2TLB hit
            self.hit_count += 1
            ppn = self.entries[vpn]
            physical_address = (ppn * self.page_size) + offset
            return physical_address, True
        else:
            # L2TLB miss
            self.miss_count += 1
            return None, False

    def insert(self, virtual_address, physical_address):
        """
        Insert a new entry into the L2TLB.

        Args:
            virtual_address: Virtual address
            physical_address: Corresponding physical address
        """
        vpn = virtual_address // self.page_size
        ppn = physical_address // self.page_size

        # Simple FIFO replacement if TLB is full
        if len(self.entries) >= self.size:
            # Remove the first entry (oldest)
            self.entries.pop(next(iter(self.entries)))

        # Add the new entry
        self.entries[vpn] = ppn

    def flush(self):
        """
        Flush all entries from the L2TLB.
        """
        self.entries.clear()

    def get_stats(self):
        """
        Return statistics about L2TLB usage.

        Returns:
            dict: Statistics including access count, hit rate, and miss rate
        """
        hit_rate = (self.hit_count / self.access_count) if self.access_count > 0 else 0
        miss_rate = (
            (self.miss_count / self.access_count) if self.access_count > 0 else 0
        )

        return {
            "access_count": self.access_count,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "miss_rate": miss_rate,
        }
