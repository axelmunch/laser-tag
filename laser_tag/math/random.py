from random import randint, random, seed


def set_seed(seed_value):
    """Set the seed for the random number generation"""
    seed(seed_value)


def random_int(min_value: int, max_value: int) -> int:
    """Random integer between min_value and max_value (inclusive)"""
    if min_value > max_value:
        min_value, max_value = max_value, min_value
    return randint(min_value, max_value)


def random_float(min_value: float, max_value: float) -> float:
    """Random number between min_value and max_value"""
    return random() * (max_value - min_value) + min_value
