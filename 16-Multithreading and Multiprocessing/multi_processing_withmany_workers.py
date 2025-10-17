import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    """Simulate CPU work"""
    result = sum(i * i for i in range(n))
    return result

if __name__ == "__main__":
    tasks = [5000000] * 100  # 100 CPU-intensive tasks
    
    # Scenario 1: 100 workers
    print("Creating pool with 100 workers...")
    start = time.time()
    with ProcessPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(cpu_task, tasks))
    time_100 = time.time() - start
    print(f"Time with 100 workers: {time_100:.2f}s")
    print(f"  - Created: 100 processes")
    print(f"  - Active at once: ~6-12")
    print(f"  - Others: Waiting/context switching")
    print(f"  - Overhead: High (process creation + switching)\n")
    
    # Scenario 2: 6 workers
    print("Creating pool with 6 workers...")
    start = time.time()
    with ProcessPoolExecutor(max_workers=12) as executor:
        results = list(executor.map(cpu_task, tasks))
    time_6 = time.time() - start
    print(f"Time with 6 workers: {time_6:.2f}s")
    print(f"  - Created: 6 processes")
    print(f"  - Active at once: 6")
    print(f"  - Others: None (all working)")
    print(f"  - Overhead: Minimal\n")
    
    print(f"Difference: {((time_100 - time_6) / time_6 * 100):.1f}% {'slower' if time_100 > time_6 else 'faster'} with 100 workers")