"""
    Type-related utilities
"""

import re

def parse_reference_key(key, strtok=':'):
    name, attr = key.split(strtok)
    name_pattern = r"^__[a-zA-Z0-9_ \.\-\(\)]+__$"
    if not re.search(name_pattern, name):
        raise ValueError(f"Invalid reference {name}")

    return name.strip('_'), attr

if __name__ == "__main__":
    key = "__UDTanMas__:max_flow"

    name, attr = parse_reference_key(key)
    print(f"name: {name}  attr: {attr}")
