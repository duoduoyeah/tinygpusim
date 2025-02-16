from ..computation_entities import Kernel, Workgroup
from typing import List, Optional
from ..shader import ShaderPipeInput
from collections import deque


class AsyncComputeEngine:
    """
    Handles asynchronous compute tasks across CUs
    execte one kernel at a time
    Args:
        num_cus (int): Number of compute units to manage
    Attributes:
        task_queue: Pending compute tasks
        active_tasks: Currently executing tasks
        workgroup_queue: Queue of workgroups
        is_workgroup_queue_empty: Flag to indicate if the workgroup queue is empty
    """

    def __init__(self, id: int):
        self.id = id
        self.kernel: Optional[Kernel] = None
        self._available = True
        self.workgroup_queue: deque[Workgroup] = deque()
        self.workgroup_queue_state = "empty"

    @property
    def available(self) -> bool:
        return self._available

    def receive_kernel(self, kernel: Kernel):
        self.kernel = kernel
        self.update_state()

    def finish_kernel(self):
        self.kernel = None
        self.update_state()

    def update_state(self):
        if self.kernel is not None:
            self.update_available()
            self.update_workgroup_queue_state()
        else:
            self.update_available()
            self.update_workgroup_queue_state()

    def update_workgroup_queue_state(self):
        if len(self.workgroup_queue) == 0:
            self.workgroup_queue_state = "empty"
        else:
            self.workgroup_queue_state = "active"

    def break_kernel(self) -> List[Workgroup]:
        """Break kernel into workgroups"""
        if self.kernel is not None:
            workgroup_num = 100
            workgroups = [Workgroup(kernel=self.kernel) for _ in range(workgroup_num)]
            self.workgroup_queue.extend(workgroups)
        else:
            raise ValueError("No kernel to break")

    def pass_workgroup(self, shader_pipe_input: ShaderPipeInput):
        """
        pass a workgroup to the shader engine
        before pass, check if the workgroup_pass_flag is True
        """
        if self.workgroup_queue_state == "active":
            shader_pipe_input.get_workgroup(self.workgroup_queue.popleft())
            if len(self.workgroup_queue) == 0:
                self.finish_kernel()

    def update_available(self):
        """Update the availability of the compute unit"""
        if self.kernel is None:
            self._available = True
        else:
            self._available = False
