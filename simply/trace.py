"""
AST capture and parameter serialization functionality for simply.

Provides factory functions to create isolated tracers for entry-point based DSLs.

Key concepts:
1. trace_and_trace_cap() - Creates a tracer system with both @trace and @trace_cap
   - @trace: Captures AST only (for internal functions)
   - @trace_cap: Captures AST + serializes parameters (for entry points)

2. make_tracer() - Simple tracer for module-local traces (legacy compatible)

This design supports complete program compilation where:
- Entry points capture both code structure and external parameters
- Internal functions capture code structure only
- Haskell gets the full program for compilation to execution engines
"""

from typing import Callable, TypeVar, Tuple, Dict, Any, Optional
from functools import wraps
import inspect
import ast
import json
import os
import textwrap
from datetime import datetime
from .parse_stmt import parse
from .stmt import AbsStmt

T = TypeVar("T", bound=Callable)


class ParameterSerializer:
    """Handles serialization of Python values to JSON-compatible format."""
    
    @staticmethod
    def serialize_value(value: Any) -> Dict[str, Any]:
        """Serialize a Python value to a JSON-compatible dictionary."""
        if value is None:
            return {"type": "none", "value": None}
        if isinstance(value, bool):
            return {"type": "bool", "value": value}
        if isinstance(value, int):
            return {"type": "int", "value": value}
        if isinstance(value, float):
            return {"type": "float", "value": value}
        if isinstance(value, str):
            return {"type": "str", "value": value}
        if isinstance(value, list):
            return {
                "type": "list",
                "length": len(value),
                "element_type": ParameterSerializer._infer_element_type(value),
                "values": [ParameterSerializer.serialize_value(v) for v in value]
            }
        if isinstance(value, tuple):
            return {
                "type": "tuple",
                "length": len(value),
                "values": [ParameterSerializer.serialize_value(v) for v in value]
            }
        if isinstance(value, dict):
            return {
                "type": "dict",
                "keys": list(value.keys()),
                "values": {k: ParameterSerializer.serialize_value(v) for k, v in value.items()}
            }
        if hasattr(value, '__dict__'):
            return {
                "type": "object",
                "class": value.__class__.__name__,
                "attributes": {k: ParameterSerializer.serialize_value(v) 
                              for k, v in value.__dict__.items()}
            }
        return {"type": "unknown", "repr": repr(value)}
    
    @staticmethod
    def _infer_element_type(lst: list) -> str:
        if not lst:
            return "unknown"
        types = set(type(x).__name__ for x in lst[:10])
        if len(types) == 1:
            return list(types)[0]
        return "mixed"


def trace_and_trace_cap(
    output_dir: str = "./output",
    indent: int = 2
) -> Tuple[Callable, Callable, Dict[str, AbsStmt], Callable]:
    """
    Create a complete tracer system with both @trace and @trace_cap decorators.
    
    This is the recommended factory for entry-point based DSLs. It provides:
    - @trace: For internal functions (captures AST only)
    - @trace_cap: For entry points (captures AST + serializes parameters)
    
    Both decorators write to the same trace dictionary, giving Haskell the complete
    program structure for compilation.
    
    Args:
        output_dir: Directory for output files (params, AST, manifest)
        indent: JSON indentation level
    
    Returns:
        A tuple of (trace_cap, trace, trace_dict, get_run_info) where:
        - trace_cap: Decorator for entry points (AST + parameter capture)
        - trace: Decorator for internal functions (AST only)
        - trace_dict: Shared dictionary storing all captured ASTs
        - get_run_info: Function to get info about the last trace_cap run
        
    Example:
        trace_cap, trace, PROGRAM_TRACE, get_run_info = trace_and_trace_cap("./output")
        
        # Entry point - captures AST + serializes parameters
        @trace_cap
        def main(data, config):
            params = sample_priors(config)  # Calls internal function
            build_likelihood(params, data)  # Calls internal function
            return params
        
        # Internal functions - capture AST only
        @trace
        def sample_priors(config):
            w = sample("w", Normal(0, 1))
            return {"w": w}
        
        @trace
        def build_likelihood(params, data):
            for i in plate("obs", len(data)):
                sample(f"y_{i}", Normal(params["w"] * data[i], 1))
    
    Output files (per trace_cap call):
        ./output/
        ├── {entry_name}.json          # AST of entry point
        ├── {entry_name}_params.json   # Serialized external parameters
        ├── {internal1}.json           # AST of internal function 1
        ├── {internal2}.json           # AST of internal function 2
        └── manifest.json              # Metadata
    """
    # Shared state for this tracer instance
    trace_dict: Dict[str, AbsStmt] = {}
    last_run_info: Dict[str, Any] = {}
    serializer = ParameterSerializer()
    
    def get_run_info() -> Dict[str, Any]:
        """Get information about the last trace_cap run."""
        return last_run_info.copy()
    
    def _capture_ast(func: T) -> Tuple[str, AbsStmt]:
        """Helper to capture AST from a function."""
        source = inspect.getsource(func)
        lines = source.split('\n')
        # Remove decorator line(s) and empty lines at start
        while lines and (not lines[0].strip() or lines[0].strip().startswith('@')):
            lines = lines[1:]
        source = '\n'.join(lines)
        source = textwrap.dedent(source)
        
        c = ast.parse(source)
        func_name = c.body[0].name
        parsed_ast = parse(c.body[0])
        
        return func_name, parsed_ast
    
    def trace(func: T) -> T:
        """
        Decorator for internal functions.
        
        Captures the function's AST and stores it in trace_dict.
        Does NOT serialize parameters (internal data comes from main).
        """
        func_name, parsed_ast = _capture_ast(func)
        trace_dict[func_name] = parsed_ast
        
        # Also write AST file immediately (internal functions don't get parameters)
        os.makedirs(output_dir, exist_ok=True)
        ast_path = os.path.join(output_dir, f"{func_name}.json")
        with open(ast_path, "w") as f:
            json.dump([parsed_ast.json], f, indent=indent)
        
        return func
    
    def trace_cap(func: T) -> T:
        """
        Decorator for entry points.
        
        Captures the function's AST AND serializes runtime parameters.
        This is for functions that receive external data from Python world.
        """
        func_name, parsed_ast = _capture_ast(func)
        trace_dict[func_name] = parsed_ast
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build parameter dictionary
            params_dict = {
                "invocation": {
                    "function": func_name,
                    "module": func.__module__,
                    "timestamp": datetime.now().isoformat(),
                },
                "args": [serializer.serialize_value(arg) for arg in args],
                "arg_names": list(inspect.signature(func).parameters.keys()),
                "kwargs": {k: serializer.serialize_value(v) for k, v in kwargs.items()}
            }
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Write parameters file
            params_path = os.path.join(output_dir, f"{func_name}_params.json")
            with open(params_path, "w") as f:
                json.dump(params_dict, f, indent=indent)
            
            # Write AST file (entry point AST)
            ast_path = os.path.join(output_dir, f"{func_name}.json")
            with open(ast_path, "w") as f:
                json.dump([parsed_ast.json], f, indent=indent)
            
            # Update manifest
            manifest_path = os.path.join(output_dir, "manifest.json")
            manifest = {
                "entry_point": func_name,
                "module": func.__module__,
                "timestamp": datetime.now().isoformat(),
                "files": {
                    "ast": f"{func_name}.json",
                    "params": f"{func_name}_params.json"
                }
            }
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=indent)
            
            # Update run info
            last_run_info.clear()
            last_run_info.update({
                "function": func_name,
                "output_dir": output_dir,
                "params_file": params_path,
                "ast_file": ast_path,
                "manifest_file": manifest_path,
                "timestamp": params_dict["invocation"]["timestamp"]
            })
            
            # Execute the function
            return func(*args, **kwargs)
        
        return wrapper
    
    return trace_cap, trace, trace_dict, get_run_info


def make_tracer() -> Tuple[Callable[[T], T], Dict[str, AbsStmt]]:
    """
    Create a simple isolated tracer with its own trace dictionary.
    
    This is the legacy/simple API. All decorated functions just capture AST.
    Use trace_and_trace_cap() for entry-point based DSLs with parameter capture.
    
    Returns:
        A tuple of (trace_decorator, trace_dict)
        
    Example:
        trace, LOCAL_TRACE = make_tracer()
        
        @trace
        def model(data):
            ...
    """
    local_trace: Dict[str, AbsStmt] = {}
    
    def trace(func: T) -> T:
        source = inspect.getsource(func)
        lines = source.split('\n')
        while lines and (not lines[0].strip() or lines[0].strip().startswith('@')):
            lines = lines[1:]
        source = '\n'.join(lines)
        source = textwrap.dedent(source)
        
        c = ast.parse(source)
        func_name = c.body[0].name
        
        local_trace[func_name] = parse(c.body[0])
        
        # Recompile to preserve runtime behavior
        obj = compile(c, filename="<ast>", mode="exec")
        exec(obj, func.__globals__)
        
        return func
    
    return trace, local_trace


# Legacy global trace for backward compatibility
GLOBAL_TRACE: Dict[str, AbsStmt] = {}


def trace(func: T) -> T:
    """
    Legacy global trace decorator.
    
    DEPRECATED: Use trace_and_trace_cap() or make_tracer() for new code.
    """
    source = inspect.getsource(func)
    lines = source.split('\n')
    while lines and (not lines[0].strip() or lines[0].strip().startswith('@')):
        lines = lines[1:]
    source = '\n'.join(lines)
    source = textwrap.dedent(source)
    
    c = ast.parse(source)
    func_name = c.body[0].name
    
    GLOBAL_TRACE[func_name] = parse(c.body[0])
    
    obj = compile(c, filename="<ast>", mode="exec")
    exec(obj, func.__globals__)
    
    return func
