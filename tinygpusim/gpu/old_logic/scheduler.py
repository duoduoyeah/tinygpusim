# Schedules and manages execution of GPU instructions across compute units
# selects active warps (groups of threads) each cycle.
# Purpose of Scheduler:
# 1. Selects active warps (groups of threads) each cycle.
# 2. Dispatches instructions to the pipeline.
# 3. Updates the pipeline states.
# 4. Updates the memory system.
# 5. Prints the pipeline state.

# TODO: Implement the scheduler.
