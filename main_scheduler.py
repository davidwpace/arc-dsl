import time
import multiprocessing
import cgre_solver as solve_task  # Importing YOUR new brain, not the old one

# --- MOCK SETTINGS (Since we are running locally) ---
# If you don't have the huge ARC JSON data file yet, we use this dummy list.
mock_problems = ["task_001", "task_002", "task_003", "task_004"]

def parallelize_runs(task_names, n_iterations):
    """
    The Scheduler Logic (Simplified for Local Run)
    """
    start_time = time.time()
    end_time = start_time + 60  # Run for 1 minute max
    
    # We assume you have 1 GPU or just use CPU if none
    n_gpus = 1 
    gpu_quotas = [100] * n_gpus # abstract 'units' of memory
    
    n_tasks = len(task_names)
    tasks_started = [False] * n_tasks
    tasks_finished = [False] * n_tasks
    processes = [None] * n_tasks
    
    print(f"Scheduler started. Managing {n_tasks} tasks on {n_gpus} 'GPUs'.")

    with multiprocessing.Manager() as manager:
        memory_dict = manager.dict()
        solutions_dict = manager.dict()
        error_queue = manager.Queue()
        
        while not all(tasks_finished):
            # Check for finished processes
            for i in range(n_tasks):
                if tasks_started[i] and not tasks_finished[i]:
                    if not processes[i].is_alive():
                        tasks_finished[i] = True
                        processes[i].join()
            
            # Start new processes
            for i in range(n_tasks):
                if not tasks_started[i]:
                    # Launch the job!
                    args = (task_names[i], "test", end_time, n_iterations, 0, memory_dict, solutions_dict, error_queue)
                    p = multiprocessing.Process(target=solve_task.solve_task, args=args)
                    p.start()
                    processes[i] = p
                    tasks_started[i] = True
                    time.sleep(0.5) # Stagger starts
            
            time.sleep(0.1)

        print("All tasks completed.")
        return solutions_dict

if __name__ == '__main__':
    # Run the scheduler on our mock data
    solutions = parallelize_runs(mock_problems, n_iterations=1)
    print("Final Solutions:", solutions)
