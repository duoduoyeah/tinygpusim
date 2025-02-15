# Skeleton for the GPU simulation

# The 5 stages mentioned here appear to be a simplified model for simulation:
# 1. Warp selection   -> Analogous to instruction fetch but for thread groups
# 2. Instruction dispatch -> Similar to CPU's issue stage
# 3. Pipeline state update-> Combines aspects of execute/memory stages
# 4. Memory system update -> Dedicated memory stage
# 5. Visualization        -> Debugging stage not present in real hardware

def run_gpu_simulation(instruction_stream: list):
    """
    Input:
        instruction_stream (list): A list of instructions to simulate.
    Output:
        None
    Data structure changed:
        This function updates internal scheduler states,
        pipeline stages, and memory status.
    Error:
        Raises ValueError if the instruction stream is invalid.
    """
    # Initialize pipeline stages, schedules, memory states
    warp_scheduler = initialize_scheduler()
    pipeline_stages = initialize_pipeline()
    cycle_count = 0

    # Add initial instructions to scheduler
    warp_scheduler["pending"] = instruction_stream.copy()
    warp_scheduler["completed"] = []

    # Run until all instructions are processed
    while not all_instructions_complete(instruction_stream):
        print(f"\n=== Cycle {cycle_count} ===")

        # Dispatch warps or threads
        dispatch_warps(warp_scheduler, pipeline_stages)

        # Simulate pipeline progression
        execute_pipeline(pipeline_stages)

        # Update memory states for any outstanding requests
        update_memory_system()

        # Print current pipeline state
        print_pipeline_state(pipeline_stages, warp_scheduler)

        cycle_count += 1
        if cycle_count > 10:  # Safety limit for testing
            break

    print(f"\nSimulation complete in {cycle_count} cycles.")


def initialize_scheduler():
    """
    Input:
        None
    Output:
        Returns an empty or default scheduler data structure.
    Data structure changed:
        None, this function only creates and returns a new object.
    Error:
        None
    """
    # Simplified: return dict or custom class
    return {}


def initialize_pipeline():
    """
    Input:
        None
    Output:
        Returns an initialized pipeline object or dict.
    Data structure changed:
        None, this function only creates and returns a new object.
    Error:
        None
    """
    return {
        "fetch": [],
        "decode": [],
        "execute": [],
        "memory": [],
        "write_back": [],
    }


def all_instructions_complete(instruction_stream):
    """
    Input:
        instruction_stream (list): The instructions being simulated.
    Output:
        bool: True if all instructions have finished executing,
        otherwise False.
    Data structure changed:
        None, this function only checks states.
    Error:
        None
    """
    return len(instruction_stream) == 0


def dispatch_warps(scheduler, pipeline):
    """
    Input:
        scheduler (dict): Current warp scheduler state.
        pipeline (dict): Pipeline stages.
    Output:
        None
    Data structure changed:
        scheduler or pipeline data structure is updated with new dispatches.
    Error:
        None
    """
    if (
        scheduler["pending"] and len(pipeline["fetch"]) < 2
    ):  # Max 2 instructions in fetch
        instr = scheduler["pending"].pop(0)
        pipeline["fetch"].append(instr)
        print(f"Dispatched instruction: {instr}")


def execute_pipeline(pipeline):
    """
    Input:
        pipeline (dict): Pipeline stages with instructions in each.
    Output:
        None
    Data structure changed:
        The contents of pipeline (moving instructions from one stage
        to the next).
    Error:
        None
    """
    # Simple shift for demonstration
    pipeline["write_back"] = pipeline["memory"]
    pipeline["memory"] = pipeline["execute"]
    pipeline["execute"] = pipeline["decode"]
    pipeline["decode"] = pipeline["fetch"]
    pipeline["fetch"] = []


def update_memory_system():
    """
    Input:
        None
    Output:
        None
    Data structure changed:
        Memory state is updated (e.g., queue of requests, latencies).
    Error:
        None
    """
    # Placeholder
    pass


def print_pipeline_state(pipeline, scheduler):
    """
    Input:
        pipeline (dict): Pipeline stages
        scheduler (dict): Scheduler state
    Output:
        None
    Data structure changed:
        None
    Error:
        None
    """
    print("\nPipeline State:")
    for stage, instructions in pipeline.items():
        print(f"{stage:10}: {instructions}")
    print(f"\nPending instructions: {len(scheduler['pending'])}")


# Add this at the bottom to test the simulation
if __name__ == "__main__":
    # Create some sample instructions
    test_instructions = [
        "ADD R1, R2, R3",
        "MUL R4, R1, R5",
        "LOAD R6, [R7]",
        "STORE [R8], R9",
    ]
    run_gpu_simulation(test_instructions)
