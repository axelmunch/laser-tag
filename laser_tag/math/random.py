from random import randint, random, seed


def set_seed(seed_value):
    seed(seed_value)


def random_int(min_value, max_value):
    if min_value > max_value:
        min_value, max_value = max_value, min_value
    return randint(min_value, max_value)


def random_float(min_value, max_value):
    return random() * (max_value - min_value) + min_value
