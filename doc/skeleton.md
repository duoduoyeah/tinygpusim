# Cycle-Level GPU Simulator Components

## Key Components

### **1. Front-End Fetch and Decode**
- A mechanism to read and parse instructions per cycle.
- Tracking program counters for multiple warps or threads.

### **2. Warp Scheduling / Dispatch**
- A scheduler that selects active warps (groups of threads) each cycle.
- Logic to handle branch divergence and reconvergence (SIMT model).

### **3. Pipeline Stages**
- Scoreboarding or hazard detection to ensure correct sequencing.
- Execution units or ALUs that simulate throughput and latency per cycle.

### **4. Memory Subsystem**
- Model of caches (L1, shared memory, possibly L2) and memory controllers.
- Cycle-accurate memory requests, potential coalescing, and bank conflicts.

### **5. SIMT / Thread Context Management**
- Tracking of active mask for warps (which threads in a warp are actually participating).
- Handling warps at different pipeline stages simultaneously.

### **6. Performance Metrics and Statistics Collection**
- Count cycles, instruction throughput (IPC), memory accesses, etc.

### **7. Concurrency Model**
- Model how multiple warps share and compete for SM (Streaming Multiprocessor) resources.
