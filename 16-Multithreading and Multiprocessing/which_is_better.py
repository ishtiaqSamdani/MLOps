import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    return sum(i * i * i for i in range(n))

if __name__ == "__main__":
    # Test different task sizes
    test_sizes = [100000, 500000, 1000000, 5000000, 10000000, 50000000]
    
    for size in test_sizes:
        tasks = [size] * 100
        
        start = time.time()
        with ProcessPoolExecutor(max_workers=100) as executor:
            list(executor.map(cpu_task, tasks))
        time_100 = time.time() - start
        
        start = time.time()
        with ProcessPoolExecutor(max_workers=12) as executor:
            list(executor.map(cpu_task, tasks))
        time_12 = time.time() - start
        
        winner = "100" if time_100 < time_12 else "12"
        diff = abs(time_100 - time_12)
        
        print(f"Task size: {size:>8} | 100w: {time_100:>5.2f}s | 12w: {time_12:>5.2f}s | Winner: {winner:>3} workers (by {diff:.2f}s)")