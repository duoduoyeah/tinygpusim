from typing import List
from dataclasses import dataclass


@dataclass
class Command:
    type: str
    parameters: dict[str, int]


def generate_commands(num_commands: int) -> List[Command]:
    """Generate a list of commands for GPU processing
    Args:
        num_commands (int): Number of commands to generate
    Returns:
        list: List of generated command dictionaries
    Raises:
        ValueError: If num_commands is negative
    """
    if num_commands < 0:
        raise ValueError("Number of commands must be non-negative")
    
    commands = []
    for i in range(num_commands):
        command = Command(
            type='kernel_launch' if i % 2 == 0 else 'memory_copy',
            parameters={'param1': i, 'param2': i * 2}
        )
        commands.append(command)
    
    return commands


if __name__ == "__main__":
    commands = generate_commands(10)
    for command in commands:
        print(command)
