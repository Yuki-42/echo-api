# Styleguide 

This document outlines the style guide for the Echo API.

## Comments

All code must have clear and concise comments explaining the purpose of the code. Comments should be used to explain 
the why, not the how. The how should be explained by the code itself.

Comments should be written to address the reader with the assumption that the reader is not fully familiar with the 
language or the codebase. 

A good way to think about comments is to write them as if you are explaining the code to someone who is not familiar 
with any libraries or frameworks that you are using and only has a basic understanding of the language.

## Type Annotations

All functions, methods, attributes, and variables should have type annotations. Type annotations are used to specify
exactly what type of data is expected by the code. This makes the code easier to read and understand and allows 
static analysis tools to catch potential bugs.

If code is not able to be annotated with types, it should be refactored to allow for type annotations.

## Naming Conventions

All variables, functions, and classes should be named in a way that is descriptive of their purpose.

### Variables

Variables should be named in snake_case and should be descriptive of their purpose.

Example:

```python
# Good
user_name: str = "John Doe"

# Bad
un: str = "John Doe"
```

### Functions

Functions should be named in snake_case and should be descriptive of their purpose.

Example:

```python
# Good
def get_user_name(user_id: int) -> str:
    """
    Get the name of a user by their ID.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        The name of the user.
    """
    pass

# Bad
def gun(user_id):
    pass
```

### Classes

Classes should be named in CamelCase and should be descriptive of their purpose.

Example:

```python
# Good
class User:
    """
    A class representing a user.
    """
    pass

# Bad
class U:
    pass
```

### Constants

Constants should be named in ALL_CAPS and should be descriptive of their purpose.

Example:

```python
# Good
MAX_RETRIES: int = 3

# Bad
mr = 3
```

## Docstrings

All functions, methods, and classes should have a docstring that explains their purpose, arguments, and return values.

Docstrings must be compliant with the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

Docstrings should be written in the following format:

```python
def function_name(arg1: type, arg2: type) -> return_type:
    """
    A short description of the function.
    
    Args:
        arg1: A description of arg1.
        arg2: A description of arg2.
        
    Returns:
        A description of the return value.
    """
    pass
```

## File Headers

All code files must have a multiline comment at the top of the file that includes the following information:

- File name
- Author
- Date
- Description

After the multiline comment, there should be a blank line before the next section of the header.

Every file must then have 4 single line comments separated by a blank line.

1. `Standard Library Imports`
2. `Third Party Imports`
3. `Local Imports`
4. `Constants`

The constants section should always contain an `__all__` variable that lists all the functions and classes that are exported by the file.

Example:

```python
"""
File: echo.py
Author: John Doe
Date: 01/01/2020
Description: This file contains the implementation of the Echo API.
"""

# Standard Library Imports

# Third Party Imports

# Local Imports

# Constants
__all__ = []
```

