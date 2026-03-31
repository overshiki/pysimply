from simply.trace import *

@trace
def test(x: int) -> int:
    return x + 1

print(test(2))
for k, v in GLOBAL_TRACE.items():
    print(v.sexp)
    print(v.json)