def greatest_product(num, window_size):

    n = num
    prod = after_zero = 1
    max_so_far = -1
    running_window = deque()

    while n:

        n, r = divmod(n, 10)
        current_window_size = len(running_window)
        prev = running_window.popleft() if current_window_size == window_size else 1

        if current_window_size == window_size - 1:
            prod = after_zero

        prod, after_zero, running_window = compute_window(r, prod, after_zero, running_window, prev)

        # update max_so_far
        if prod > max_so_far:
            max_so_far = prod

    return max_so_far