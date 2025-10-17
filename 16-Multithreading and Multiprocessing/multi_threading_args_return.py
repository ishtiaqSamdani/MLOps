import threading

def calculate(operation, a, b, results, thread_id, verbose=False):
    if operation == "add":
        result = a + b
    elif operation == "multiply":
        result = a * b
    
    if verbose:
        print(f"{operation}: {a} and {b} = {result}")
    
    results[thread_id] = result

results = {}

t1 = threading.Thread(
    target=calculate,
    args=("add", 5, 3, results, "t1"),
    kwargs={"verbose": True}
)

t1.start()
t1.join()

print(f"Result from thread: {results['t1']}")  