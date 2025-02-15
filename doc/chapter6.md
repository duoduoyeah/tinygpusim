GPU_Blocks/
├── Controlling/           # Blocks responsible for CPU interaction and control
│   ├── CommandProcessor/   # Receives and delegates commands from the CPU
│   │   ├── ... (Source files, headers, documentation related to Command Processor)
│   │   └── ...
│   ├── ACE/                # Asynchronous Compute Engine - handles kernel launching
│   │   ├── ... (Source files, headers, documentation related to ACE)
│   │   └── ...
│   ├── DMA/                # Direct Memory Access - handles memory copying
│   │   ├── ... (Source files, headers, documentation related to DMA)
│   │   └── ...
│   └── ... (Other controlling blocks, if any)
│
├── Shader/              # User-programmable shader blocks
│   ├── ... (Source files, headers, documentation related to Shaders)
│   └── ...
│
├── Memory/              # Memory-related blocks
│   ├── ... (Source files, headers, documentation related to Memory management)
│   └── ...
│
├── Documentation/       # Overall documentation
│   ├── Overview.md      # High-level overview of the GPU architecture
│   └── ...
│
└── ... (Other top-level files, build scripts, etc.)

