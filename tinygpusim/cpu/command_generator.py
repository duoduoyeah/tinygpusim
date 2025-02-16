from dataclasses import dataclass


@dataclass
class Command:
    type: str
    parameters: dict[str, int]
