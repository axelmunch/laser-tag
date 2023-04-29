eval_banned_elements = [
    "import ",
    "(",
    ";",
    "=",
]


def safe_eval(data, debug=False):
    normalized_data = str(data).strip().lower()
    for element in eval_banned_elements:
        if element in normalized_data:
            if debug:
                print(f'EVAL banned element "{element}" found in {data}')
            return None
    try:
        return eval(data, {}, {})
    except Exception as e:
        if debug:
            print(f"EVAL {e}. Evaluating: {data}")
        return None
