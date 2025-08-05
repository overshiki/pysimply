from simply.trace import *

@trace
def test(x: int) -> int:
    return x + 1

print(test(2))