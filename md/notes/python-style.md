# Python Coding Style Guide

This guide outlines a clean, readable, and maintainable approach to Python development. It prioritizes explicit typing, specific exception handling, modular structure, dependency management, and rigorous testing.

---

## 1. **Type Hints for Readability and Reliability**

Using type hints improves code readability and helps detect errors early, especially in large codebases or monorepos with complex interactions.

#### Example:
```python
def add_numbers(a: int, b: int) -> int:
    return a + b
```

---

## 2. **Purposeful Exception Handling**

Handle exceptions only when there’s a specific response or corrective action. Avoid broad `except Exception as e` blocks unless absolutely necessary, and **never** end a function with a catch-all exception handler.

#### Preferred:
```python
def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()
```

#### Avoid:
```python
def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}")
        return ""
```

---

## 3. **Using Decorators for Consistent Exception Handling**

If a consistent error-handling approach is necessary, use decorators rather than embedding try/except blocks directly within functions. This keeps the business logic clean and separates concerns effectively.

#### Example:
```python
import functools
import logging

def log_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception in {func.__name__}: {e}")
            raise  # Re-raise to allow normal exception handling flow
    return wrapper

@log_exceptions
def process_data(data: str) -> int:
    return int(data)  # May raise ValueError if data is invalid
```

---

## 4. **Avoid Magic Strings and Numbers**

"Magic strings" and numbers—hardcoded values that appear without context—make code less readable and harder to maintain. Use constants or enums to avoid these.

#### Example:
```python
# Define constants
DEFAULT_TIMEOUT = 30
ERROR_MESSAGE = "An error occurred"

def connect(timeout: int = DEFAULT_TIMEOUT) -> None:
    print(ERROR_MESSAGE)
```

Alternatively, enums can be helpful for clearly defined values, especially when modeling states or fixed choices.

#### Using Enums:
```python
from enum import Enum

class Status(Enum):
    SUCCESS = "success"
    ERROR = "error"

def log_status(status: Status) -> None:
    print(f"Operation ended with status: {status.value}")
```

---

## 5. **Clean Dependencies: No Circular Imports**

Circular dependencies often arise in monorepos or complex applications. These dependencies can be challenging to debug and maintain. Avoid them by:
- Structuring modules so each has a single responsibility.
- Using dependency injection when necessary to decouple components.
- Importing within functions instead of globally if certain imports cause circularity (only as a last resort).

#### Example:
```python
# Avoid this pattern if two modules import each other
# Instead, refactor shared functionality into a separate utility module
```

---

## 6. **Extreme Modularization in Monorepos**

In monorepos, each module or package should encapsulate a specific feature or function. This ensures scalability and keeps the code manageable. Here’s how:
- **Define clear boundaries** for each package or module.
- **Limit inter-package dependencies** and, if necessary, make them explicit in the module’s `__init__.py` file.
- **Use shared modules** for commonly needed functions or utilities, keeping core logic within its package.

#### Directory Structure for Modularization:
```plaintext
.
└── packages
    ├── feature_one
    │   ├── core_logic.py
    │   ├── helpers.py
    │   └── __init__.py
    ├── feature_two
    │   ├── processing.py
    │   ├── validations.py
    │   └── __init__.py
    └── shared_utils
        ├── utils.py
        └── __init__.py
```

---

## 7. **Every File is Unit Tested**

Maintain high test coverage by creating a unit test file for each Python file. Name each test file as `test_<filename>.py` and store it in the same directory.

#### Example:
```plaintext
feature_one/
├── core_logic.py
├── helpers.py
└── test_core_logic.py  # Unit tests for core_logic.py
```

### Test Structure and Style
- Each function should have at least one unit test.
- Use **mocking** where necessary to isolate tests from external dependencies (like databases or network services).
- **Name tests clearly** to describe what they’re validating.

#### Example Unit Test:
```python
# test_core_logic.py
import pytest
from feature_one.core_logic import some_function

def test_some_function():
    result = some_function(5)
    assert result == expected_value
```

---

## 8. **Prioritize Readability and Maintainability**

Readable code is critical for maintainability. Avoid terse or ambiguous code. Use meaningful variable names, limit line length, and follow consistent formatting.

#### Example:
```python
# Good
total_revenue = sum(monthly_revenues)

# Avoid ambiguous or overly terse code
x = sum(y)
```

---

## 9. **Efficient Use of Context Managers and Standard Libraries**

Use context managers for managing resources like files or network connections to ensure clean-up actions and reduce the need for extensive error handling.

#### Example:
```python
with open("data.txt", "r") as file:
    data = file.read()
```

---

## Summary: Python Style at a Glance

- **Type Hints**: Use them everywhere to make code clear and error-resistant.
- **Specific Exception Handling**: Catch exceptions only when there’s a meaningful action.
- **Avoid Magic Strings and Numbers**: Use constants or enums to improve readability.
- **Clean Dependencies**: No circular imports; structure code to be self-contained.
- **Modularize Aggressively**: Each module should have a single responsibility.
- **Test Each File**: Use `test_<filename>.py` for thorough, isolated unit tests.
- **Prioritize Readability**: Write descriptive, maintainable code.
- **Use Context Managers**: Simplify resource management without extra error handling.

This style guide helps ensure that your Python codebase is readable, modular, and reliable, supporting clean and scalable development.