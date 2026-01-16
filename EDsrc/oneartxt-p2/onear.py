# onear.py - Global State Container
# Provides access to data via ID (Index) or KEY (String)

# The Singleton Data Store
data = []      # The 1D Array of values (str/int/etc)
keys = {}      # Mapping: 'keyname' -> int_index  // not a 1D array key to idx 

def init(size=1000):
    """Initialize empty data array"""
    global data, keys
    data = [''] * size
    keys = {}

def register_key(key_name, index):
    """
    Registers a key name to an index.
    Example: register_key('c_btn20', 20)
    """
    global keys
    keys[key_name] = int(index)

def oneindex(key_or_name):
    """
    Returns the integer index for a given key string.
    If input is already int (or digit string), returns int.
    Returns -1 if not found.
    """
    # 1. If it's already an integer, return it
    if isinstance(key_or_name, int):
        return key_or_name
    
    # 2. If it's a digit string "22", return 22
    if isinstance(key_or_name, str) and key_or_name.isdigit():
        return int(key_or_name)

    # 3. Lookup name in keys dict
    if key_or_name in keys:
        return keys[key_or_name]
    
    # 4. Error / Not found
    print(f"ONEAR ERROR: Key '{key_or_name}' not found.")
    return -1

def onearkey(key_or_idx):
    """
    Universal Getter:
    onearkey(22)       -> returns data[22]
    onearkey('c_btn')  -> returns data[keys['c_btn']]
    """
    idx = oneindex(key_or_idx)
    
    if idx == -1:
        return None
        
    if 0 <= idx < len(data):
        return data[idx]
    else:
        print(f"ONEAR ERROR: Index {idx} out of bounds (Size: {len(data)})")
        return None
