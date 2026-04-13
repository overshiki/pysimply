# Trace Design: From Global to Local

## Problem Statement

The current `simply.trace` module uses a single global dictionary `GLOBAL_TRACE` to store captured ASTs. This causes issues:

1. **Hidden shared state**: All modules using `@trace` write to the same dictionary
2. **Unclear ownership**: Can't tell which module captured which function
3. **Name collisions**: Functions with same name in different modules overwrite each other
4. **Misleading code**: The pattern `REGRESSION_TRACE.update(GMM_TRACE)` suggests merging separate dicts, but they're actually the same object

## Current Implementation

```python
# simply/trace.py
GLOBAL_TRACE = {}  # Module-level singleton

def trace(func):
    GLOBAL_TRACE[func_name] = parse(...)  # All decorators write here
    return func
```

When multiple modules import `trace`:
```python
# model_regression.py
from simply.trace import trace, GLOBAL_TRACE as REGRESSION_TRACE

# model_gmm.py  
from simply.trace import trace, GLOBAL_TRACE as GMM_TRACE

# REGRESSION_TRACE is GMM_TRACE is simply.trace.GLOBAL_TRACE  # True!
```

## Design Options

### Option 1: Decorator Factory (Recommended)

Create isolated tracer instances per module.

**Implementation:**
```python
# simply/trace.py
def make_tracer():
    """Create a new isolated tracer with its own trace dictionary."""
    local_trace = {}
    
    def trace(func):
        import inspect
        import ast
        from simply.parse_stmt import parse
        
        lines, lineno = inspect.getsourcelines(func)
        source = inspect.cleandoc("".join(lines)).removeprefix("@trace\n")
        c = ast.parse(source)
        func_name = c.body[0].name
        
        local_trace[func_name] = parse(c.body[0])
        
        # Recompile and exec to preserve runtime behavior
        obj = compile(c, filename="<ast>", mode="exec")
        exec(obj)
        
        return func
    
    return trace, local_trace
```

**Usage:**
```python
# model_regression.py
from simply.trace import make_tracer

trace, LOCAL_TRACE = make_tracer()

@trace
def model(data):
    ...

@trace
def guide(data):
    ...

# LOCAL_TRACE == {'model': ..., 'guide': ...}
```

**Pros:**
- ✓ Complete isolation between modules
- ✓ No global state
- ✓ Clear ownership: each module owns its trace dict
- ✓ Simple API: `trace, trace_dict = make_tracer()`
- ✓ Works with existing `@trace` decorator syntax
- ✓ No name collisions possible

**Cons:**
- ✗ Can't easily trace across module boundaries with same tracer
- ✗ Need to pass `trace` to other modules if shared capture needed

**Best for:** Most use cases - each model module manages its own traces.

---

### Option 2: Context Manager

Use a context manager to establish a trace scope.

**Implementation:**
```python
# simply/trace.py
import contextvars
from contextlib import contextmanager

_current_trace = contextvars.ContextVar('current_trace', default=None)
GLOBAL_TRACE = {}  # Fallback

def trace(func):
    import inspect
    import ast
    from simply.parse_stmt import parse
    
    lines, lineno = inspect.getsourcelines(func)
    source = inspect.cleandoc("".join(lines)).removeprefix("@trace\n")
    c = ast.parse(source)
    func_name = c.body[0].name
    
    target_trace = _current_trace.get()
    if target_trace is not None:
        target_trace[func_name] = parse(c.body[0])
    else:
        GLOBAL_TRACE[func_name] = parse(c.body[0])  # Fallback
    
    obj = compile(c, filename="<ast>", mode="exec")
    exec(obj)
    return func

@contextmanager
def local_trace_scope():
    local_trace = {}
    token = _current_trace.set(local_trace)
    try:
        yield local_trace
    finally:
        _current_trace.reset(token)
```

**Usage:**
```python
# model_regression.py
from simply.trace import local_trace_scope, trace

with local_trace_scope() as REGRESSION_TRACE:
    @trace
    def model(data):
        ...
    
    @trace
    def guide(data):
        ...

# REGRESSION_TRACE == {'model': ..., 'guide': ...}
```

**Pros:**
- ✓ Explicit scope for trace collection
- ✓ Can nest scopes if needed
- ✓ Automatic cleanup on exit

**Cons:**
- ✗ Requires wrapping code in `with` block
- ✗ Less intuitive for module-level definitions
- ✗ ContextVar overhead (minor)

**Best for:** Temporary/ad-hoc tracing sessions, not module-level definitions.

---

### Option 3: Class-Based Tracer

Use a class instance as the decorator.

**Implementation:**
```python
# simply/trace.py
class Tracer:
    """A tracer that captures decorated function ASTs to a local dictionary."""
    
    def __init__(self):
        self.trace_dict = {}
    
    def __call__(self, func):
        import inspect
        import ast
        from simply.parse_stmt import parse
        
        lines, lineno = inspect.getsourcelines(func)
        source = inspect.cleandoc("".join(lines)).removeprefix("@tracer\n")
        c = ast.parse(source)
        func_name = c.body[0].name
        
        self.trace_dict[func_name] = parse(c.body[0])
        
        obj = compile(c, filename="<ast>", mode="exec")
        exec(obj)
        return func
    
    def __getitem__(self, key):
        return self.trace_dict[key]
    
    def __iter__(self):
        return iter(self.trace_dict)
    
    def items(self):
        return self.trace_dict.items()
    
    def __len__(self):
        return len(self.trace_dict)
```

**Usage:**
```python
# model_regression.py
from simply.trace import Tracer

tracer = Tracer()

@tracer  # Note: uses @tracer not @trace
def model(data):
    ...

@tracer
def guide(data):
    ...

# tracer.trace_dict == {'model': ..., 'guide': ...}
```

**Pros:**
- ✓ Object-oriented design
- ✓ Can extend with methods (dump_json, etc.)
- ✓ Can have multiple tracers in same module

**Cons:**
- ✗ Decorator syntax changes from `@trace` to `@tracer`
- ✗ More verbose
- ✗ Need to remember instance name

**Best for:** Complex scenarios needing multiple tracers or additional methods.

---

### Option 4: Namespaced Global Trace

Keep global but organize by module automatically.

**Implementation:**
```python
# simply/trace.py
GLOBAL_TRACE = {}  # {'module_name': {'func_name': ast}}

def trace(func):
    import inspect
    import ast
    from simply.parse_stmt import parse
    
    # Get calling module name
    import sys
    frame = sys._getframe(1)
    module_name = frame.f_globals.get('__name__', 'unknown').split('.')[-1]
    
    if module_name not in GLOBAL_TRACE:
        GLOBAL_TRACE[module_name] = {}
    
    lines, lineno = inspect.getsourcelines(func)
    source = inspect.cleandoc("".join(lines)).removeprefix("@trace\n")
    c = ast.parse(source)
    func_name = c.body[0].name
    
    GLOBAL_TRACE[module_name][func_name] = parse(c.body[0])
    
    obj = compile(c, filename="<ast>", mode="exec")
    exec(obj)
    return func

def get_module_trace(module_name):
    """Get trace dict for a specific module."""
    return GLOBAL_TRACE.get(module_name, {})
```

**Usage:**
```python
# model_regression.py
from simply.trace import trace  # Just import trace

@trace
def model(data):
    ...

# In run.py:
from simply.trace import GLOBAL_TRACE, get_module_trace

regression_trace = get_module_trace('model_regression')
gmm_trace = get_module_trace('model_gmm')
# Or access GLOBAL_TRACE['model_regression'] directly
```

**Pros:**
- ✓ Simple import: just `from simply.trace import trace`
- ✓ Automatic organization by module
- ✓ No setup required

**Cons:**
- ✗ Still uses global state (just better organized)
- ✗ Module name detection can be fragile
- ✗ Can't have multiple tracers per module
- ✗ Less explicit - magic organization

**Best for:** Backward compatibility, simple use cases.

---

## Comparison Matrix

| Feature | Option 1 (Factory) | Option 2 (Context) | Option 3 (Class) | Option 4 (Namespace) |
|---------|-------------------|-------------------|------------------|---------------------|
| No global state | ✓ | ✓ | ✓ | ✗ |
| Simple API | ✓ | ✗ | ✓ | ✓ |
| Existing `@trace` syntax | ✓ | ✓ | ✗ | ✓ |
| Multiple tracers per module | ✓ | ✓ | ✓ | ✗ |
| Automatic module organization | ✗ | ✗ | ✗ | ✓ |
| No setup code needed | ✗ | ✗ | ✗ | ✓ |
| Works across module boundaries | ✗ | ✗ | ✓ | ✓ |
| Explicit scope control | ✗ | ✓ | ✗ | ✗ |

## Recommendation

**Use Option 1 (Decorator Factory)** for most cases because:

1. **Clear ownership**: `trace, TRACE = make_tracer()` makes it obvious where traces go
2. **Zero magic**: No hidden global state, no frame inspection, no context variables
3. **Testability**: Easy to create isolated tracers in unit tests
4. **Familiar syntax**: Keeps `@trace` decorator pattern
5. **Pythonic**: Factory functions are idiomatic Python

The slight verbosity (`trace, TRACE = make_tracer()`) is actually a benefit - it makes the trace destination explicit.

## Migration Guide

### From Global to Option 1

**Before:**
```python
# simply/trace.py
GLOBAL_TRACE = {}

def trace(func): ...

# model.py
from simply.trace import trace, GLOBAL_TRACE

@trace
def model(): ...
```

**After:**
```python
# simply/trace.py
def make_tracer():
    local_trace = {}
    def trace(func): ...
    return trace, local_trace

# model.py
from simply.trace import make_tracer

trace, LOCAL_TRACE = make_tracer()

@trace
def model(): ...
```

**In runner:**
```python
# Before: confusing merge of same dict
GLOBAL_TRACE = {}
GLOBAL_TRACE.update(REGRESSION_TRACE)
GLOBAL_TRACE.update(GMM_TRACE)

# After: meaningful merge of distinct dicts
ALL_TRACES = {}
ALL_TRACES.update(REGRESSION_TRACE)
ALL_TRACES.update(GMM_TRACE)
```
