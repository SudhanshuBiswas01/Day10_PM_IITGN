# decorators.py
# Part B - Building Decorators from Scratch
# Self-studied from Python docs on closures, functools.wraps

import time
import functools


# -----------------------------------------------
# @timer decorator
# -----------------------------------------------

def timer(func):
    """Measures and prints the execution time of the decorated function.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function that prints execution time after calling func.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f"[timer] '{func.__name__}' took {elapsed:.6f} seconds")
        return result
    return wrapper


# -----------------------------------------------
# @logger decorator
# -----------------------------------------------

def logger(func):
    """Logs function name, arguments, and return value on each call.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function that prints call info before and after execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[logger] Calling '{func.__name__}' with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[logger] '{func.__name__}' returned: {result}")
        return result
    return wrapper


# -----------------------------------------------
# @retry decorator (with max_attempts parameter)
# -----------------------------------------------

def retry(max_attempts=3):
    """Retries a function up to max_attempts times if it raises an exception.

    Args:
        max_attempts: Maximum number of retry attempts. Defaults to 3.

    Returns:
        A decorator that wraps func with retry logic.

    Usage:
        @retry(max_attempts=5)
        def unstable_function():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"[retry] Attempt {attempt}/{max_attempts} failed: {e}")
            # all attempts exhausted
            print(f"[retry] All {max_attempts} attempts failed for '{func.__name__}'")
            raise last_exception
        return wrapper
    return decorator


# -----------------------------------------------
# Demo / testing the decorators
# -----------------------------------------------

if __name__ == "__main__":

    # --- timer demo ---
    @timer
    def slow_sum(n):
        total = 0
        for i in range(n):
            total += i
        return total

    print("=== Timer Demo ===")
    print(slow_sum(500000))

    # --- logger demo ---
    @logger
    def add(a, b):
        return a + b

    print("\n=== Logger Demo ===")
    add(10, 20)
    add(3, b=7)

    # --- retry demo ---
    call_count = [0]

    @retry(max_attempts=3)
    def flaky_function():
        call_count[0] += 1
        if call_count[0] < 3:
            raise ValueError(f"Simulated failure on attempt {call_count[0]}")
        return "Success on attempt 3"

    print("\n=== Retry Demo ===")
    print(flaky_function())

    # retry that always fails
    @retry(max_attempts=2)
    def always_fails():
        raise RuntimeError("This always fails")

    print("\n=== Retry Always Fails Demo ===")
    try:
        always_fails()
    except RuntimeError as e:
        print(f"Caught expected error: {e}")
