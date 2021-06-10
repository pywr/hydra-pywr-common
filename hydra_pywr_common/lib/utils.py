"""
    Type-related utilities
"""

import re

"""
  Enforces canonical name format on references.
"""
def parse_reference_key(key, strtok=':'):
    name, attr = key.split(strtok)
    name_pattern = r"^__[a-zA-Z0-9_ \.\-\(\)]+__$"
    if not re.search(name_pattern, name):
        raise ValueError(f"Invalid reference {name}")

    return name.strip('_'), attr
