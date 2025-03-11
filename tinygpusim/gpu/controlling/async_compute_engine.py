from ..computation_entities import Kernel, Workgroup
from typing import List, Optional, Dict
from ..shader import ShaderPipeInput
from collections import deque


class AsyncComputeEngine:
    """
    Handles asynchronous compute tasks across CUs
    
    ACEs are responsible for:
    1. Breaking kernels into workgroups
    2. Dispatching workgroups to SPIs
    3. Managing concurrent kernel execution
    
    Args:
        id (int): Unique identifier for this ACE
        
    Attributes:
        id: Unique identifier
        kernel: Currently executing kernel
        workgroup_queue: Queue of workgroups ready for dispatch
        workgroup_queue_state: Current state of the workgroup queue
        resource_limits: Resource limits for workgroups
    """

    def __init__(self, id: int):
        self.id = id
        self.kernel: Optional[Kernel] = None
        self._available = True
        self.workgroup_queue: deque[Workgroup] = deque()
        self.workgroup_queue_state = "empty"
        
        # Track resources to prevent deadlock situations described in the text
        self.resource_limits = {
            "max_active_workgroups": 64,  # Example value
            "max_wavefront_slots": 40,    # Example value
            "max_sgpr_per_cu": 800,       # Example value
            "max_vgpr_per_cu": 256,       # Example value
            "max_lds_per_cu": 64 * 1024   # Example value (64KB)
        }
        
        # Track active workgroups for each kernel
        self.active_kernel_workgroups: Dict[str, int] = {}

    @property
    def available(self) -> bool:
        return self._available

    def receive_kernel(self, kernel: Kernel):
        """
        Receive a kernel launch command and prepare for execution
        
        Args:
            kernel (Kernel): The kernel to execute
        """
        self.kernel = kernel
        
        # Initialize tracking for this kernel
        if kernel.name not in self.active_kernel_workgroups:
            self.active_kernel_workgroups[kernel.name] = 0
            
        # Break the kernel into workgroups and queue them
        self.break_kernel()
        self.update_state()

    def finish_kernel(self):
        """Mark the current kernel as finished and clean up"""
        if self.kernel:
            # Remove tracking for this kernel
            if self.kernel.name in self.active_kernel_workgroups:
                del self.active_kernel_workgroups[self.kernel.name]
                
        self.kernel = None
        self.update_state()

    def update_state(self):
        """Update the internal state based on current conditions"""
        self.update_available()
        self.update_workgroup_queue_state()

    def update_workgroup_queue_state(self):
        """Update the state of the workgroup queue"""
        if len(self.workgroup_queue) == 0:
            self.workgroup_queue_state = "empty"
        else:
            self.workgroup_queue_state = "active"

    def break_kernel(self) -> List[Workgroup]:
        """
        Break kernel into workgroups
        
        This method calculates the appropriate number of workgroups based on
        the kernel's grid dimensions and creates workgroup objects
        """
        if self.kernel is None:
            raise ValueError("No kernel to break")
            
        # In a real implementation, we would calculate workgroups based on:
        # 1. The kernel's grid dimensions
        # 2. The workgroup size specified by the kernel
        
        # For simplicity, we're using a fixed number
        workgroup_num = min(100, self.resource_limits["max_active_workgroups"])
        
        # Create workgroups and add to queue
        workgroups = [Workgroup(kernel=self.kernel) for _ in range(workgroup_num)]
        self.workgroup_queue.extend(workgroups)
        
        # Update active workgroup count
        self.active_kernel_workgroups[self.kernel.name] = len(workgroups)
        
        return workgroups

    def pass_workgroup(self, shader_pipe_input: ShaderPipeInput):
        """
        Pass a workgroup to the shader engine
        
        This method is called when a shader processing unit is ready
        to receive a new workgroup
        
        Args:
            shader_pipe_input (ShaderPipeInput): The input interface for the shader
        """
        if self.workgroup_queue_state == "active":
            # Get the next workgroup from the queue
            workgroup = self.workgroup_queue.popleft()
            
            # Pass it to the shader pipe input
            if shader_pipe_input.get_workgroup(workgroup):
                # Update active workgroup count
                if self.kernel and self.kernel.name in self.active_kernel_workgroups:
                    self.active_kernel_workgroups[self.kernel.name] -= 1
                
                # If all workgroups have been dispatched, finish the kernel
                if len(self.workgroup_queue) == 0:
                    self.finish_kernel()

    def update_available(self):
        """Update the availability of the compute unit"""
        if self.kernel is None:
            self._available = True
        else:
            self._available = False
