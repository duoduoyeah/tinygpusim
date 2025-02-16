from .cpu_mem import CPUMemory
from .command_generator import Command


class CPU:
    def __init__(self, cpu: CPUMemory):
        self.cpu_mem = cpu

    def generate_commands(self, num_commands: int):
        if num_commands < 0:
            raise ValueError("Number of commands must be non-negative")

        commands = []
        for i in range(num_commands):
            command = Command(
                type="kernel_launch" if i % 2 == 0 else "memory_copy",
                parameters={"param1": i, "param2": i * 2},
            )
            commands.append(command)

        return commands
