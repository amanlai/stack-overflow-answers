from collections import deque

def compute_window(new_digit, prod, no_zero_prod, window, old_digit=1):

    # compute product for this window
    prod = prod // old_digit * new_digit
    # if the new digit is zero, restart everything (because 0*number=0)
    if new_digit == 0:
        window, prod, no_zero_prod = deque(), 0, 1
    else:
        window.append(new_digit)
        no_zero_prod = no_zero_prod // old_digit * new_digit

    return prod, no_zero_prod, window


def greatest_product(num, window_size):

    # initialize variable
    running_window = deque()
    prod = after_zero = 1

    # calculate the initial product
    for d in num[: window_size]:
        prod, after_zero, running_window = compute_window(int(d), prod, after_zero, running_window)
    # max value to beat
    max_so_far = prod

    for d in num[window_size :]:

        # in each iteration, if the window is full, pop the element that was first entered
        current_window_size = len(running_window)
        prev = running_window.popleft() if current_window_size == window_size else 1

        # if a single element is missing from window, assign the after_zero value to prod
        # (which allows us to use it for this round's product computation)
        if current_window_size == window_size - 1:
            prod = after_zero

        # computations for this iteration
        prod, after_zero, running_window = compute_window(int(d), prod, after_zero, running_window, prev)

        # update max_so_far
        if prod > max_so_far:
            max_so_far = prod

    return max_so_far