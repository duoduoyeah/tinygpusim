class L2Cache:
    """
    L2 cache in gpu is related to:
    1. crossbar()
    2. dram()
    3. dma_engine()
    """

    def __init__(self, dram, dma_engine):
        self.dram = dram
        self.dma_engine = dma_engine
