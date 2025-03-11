from dataclasses import dataclass


@dataclass
class Wavefront:
    kernel: "Kernel"
    workgroup: "Workgroup"


@dataclass
class Workgroup:
    kernel: "Kernel"


@dataclass
class Kernel:
    name: str
    args: dict
