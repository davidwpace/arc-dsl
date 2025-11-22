import time
import multiprocessing
import glob
import os
import cgre_solver as solve_task

def get_real_tasks():
    """
    Scans the downloaded folder for real ARC JSON files.
    """
    # This matches the path structure you found: ./data/data/training/
    path = "./data/data/training/*.json"
    files = glob.glob(path)
    
    if not files:
        print(f"ERROR: No files found at {path}")
        return []
    
    # CRITICAL: Sort them so runs are reproducible
    files = sorted(files)
    
    # FOR SAFETY: Only take the first 3 puzzles for this test run.
    # We don't want to burn your CPU running 400 puzzles yet.
    return files[:3]

def parallelize_runs(task_files, n_iterations):
    start_time = time.time()
    end_time = start_time + 60
    
    n_tasks = len(task_files)
    tasks_started = [False] * n_tasks
    tasks_finished = [False] * n_tasks
    processes = [None] * n_tasks
    
    print(f"Scheduler started. Loaded {n_tasks} REAL ARC puzzles from disk.")

    with multiprocessing.Manager() as manager:
        memory_dict = manager.dict()
        solutions_dict = manager.dict()
        error_queue = manager.Queue()
        
        while not all(tasks_finished):
            # Clean up finished processes
            for i in range(n_tasks):
                if tasks_started[i] and not tasks_finished[i]:
                    if not processes[i].is_alive():
                        tasks_finished[i] = True
                        processes[i].join()
            
            # Start new processes
            for i in range(n_tasks):
                if not tasks_started[i]:
                    # We pass the FULL FILE PATH as the task name now
                    task_path = task_files[i]
                    args = (task_path, "test", end_time, n_iterations, 0, memory_dict, solutions_dict, error_queue)
                    p = multiprocessing.Process(target=solve_task.solve_task, args=args)
                    p.start()
                    processes[i] = p
                    tasks_started[i] = True
                    time.sleep(0.5) 
            
            time.sleep(0.1)

        print("All tasks completed.")
        return solutions_dict

if __name__ == '__main__':
    real_tasks = get_real_tasks()
    if real_tasks:
        print(f"Selected Tasks: {[os.path.basename(t) for t in real_tasks]}")
        solutions = parallelize_runs(real_tasks, n_iterations=1)
