# interview_ready.py
# Part C - Interview Ready: LEGB, Memoize, Debug/Fix

# -----------------------------------------------
# Q2: memoize function
# -----------------------------------------------

def memoize(func):
    """Cache results of expensive function calls.

    When called with the same arguments, returns cached result
    instead of recomputing.

    Args:
        func: The function whose results should be cached.

    Returns:
        Wrapped function with caching behaviour.

    Usage:
        @memoize
        def fibonacci(n):
            ...
    """
    cache = {}  # key = args tuple, value = result

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def fibonacci(n):
    """Recursive fibonacci - fast with memoization.

    Args:
        n: The index of the fibonacci sequence.

    Returns:
        The nth fibonacci number.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# -----------------------------------------------
# Q3: Bugfix - mutable default argument + scope bug
# -----------------------------------------------

# ORIGINAL BUGGY CODE (DO NOT RUN):
# total = 0
# def add_to_cart(item, cart=[]):       # Bug 1: mutable default
#     cart.append(item)
#     total = total + len(cart)          # Bug 2: scope issue (UnboundLocalError)
#     return cart
#
# Bug 1: cart=[] is created once at function definition time.
#         Every call shares the same list object.
#         Second call to add_to_cart('banana') prints ['apple', 'banana']
#         because 'apple' is still in the list from the first call.
#
# Bug 2: total = total + len(cart) makes Python treat 'total' as a local variable
#         in this function. But we're reading it before assigning, so we get
#         UnboundLocalError: local variable 'total' referenced before assignment.
#         Using 'global total' would fix it, but that's a code smell.
#         Better approach: pass total as a parameter or return it.

# FIXED VERSION:
total = 0

def add_to_cart(item, cart=None):
    """Add item to cart and return updated cart.

    Args:
        item: Item to add.
        cart: Optional existing cart list. Defaults to a fresh empty list.

    Returns:
        Updated cart list.
    """
    if cart is None:
        cart = []           # Fix 1: create new list each call
    cart.append(item)
    return cart             # Fix 2: removed broken total logic;
                            # pass total in if needed, or track outside


# -----------------------------------------------
# Demo
# -----------------------------------------------

if __name__ == "__main__":

    # Q2 demo
    print("=== Memoize / Fibonacci ===")
    import time
    start = time.time()
    print(fibonacci(50))
    end = time.time()
    print(f"fibonacci(50) computed in {end - start:.6f}s (near instant with memoization)")

    # Q3 demo - fixed version
    print("\n=== Fixed add_to_cart ===")
    cart1 = add_to_cart('apple')
    print(cart1)            # ['apple']

    cart2 = add_to_cart('banana')
    print(cart2)            # ['banana']  -- no contamination from cart1
