
def pytest_assertrepr_compare(op, left, right):
    if op == '==' and isinstance(left, list):
        return left