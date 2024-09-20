def float_to_int(value: float):
    if not isinstance(value, float):
        return value

    if value.is_integer():
        return int(value)
    return value
