"""Time a function execution time"""

from .Timer import Timer


def timer(function):
    """@timer decorator before function declaration to enable timing"""

    def wrapper(*args, **kwargs):
        timer = Timer()
        timer.start()
        function_return_value = function(*args, **kwargs)
        timer.stop()
        print(f"{function.__name__} executed during {timer.get_time():.5f}sec.")
        return function_return_value

    return wrapper
