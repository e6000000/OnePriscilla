import p2

def get_by_key(result_array, key_name, step=5):
    """
    Retrieves the value associated with a key name from the 1D array.
    
    Schema: ID | KEY | val1 | val2 | val3 | val4
    
    Args:
        result_array: The 1D array from parse_config_file()
        key_name: The key to search for (e.g., "c_btn20", "key_10__50__")
        step: Step size (default 5)
    
    Returns:
        The value at position [key_position + 1], or None if not found
        
    Example:
        If array[20] = "c_btn20", then returns array[21] = "#3e3e42"
    """
    # Loop through array in steps
    for i in range(0, len(result_array), step):
        # Check if this position contains the key
        if result_array[i] == key_name:
            # Return the next position (val1)
            next_pos = i + 1
            if next_pos < len(result_array):
                return result_array[next_pos]
            else:
                return None
    
    return None  # Key not found


def get_by_index(result_array, index):
    """
    Retrieves the value at a specific position in the 1D array.
    
    Args:
        result_array: The 1D array from parse_config_file()
        index: Direct position number (0-based)
    
    Returns:
        The value at result_array[index], or None if out of bounds
        
    Example:
        get_by_index(result_array, 21) returns "#3e3e42"
    """
    if 0 <= index < len(result_array):
        return result_array[index]
    else:
        return None


def get_key_block(result_array, key_name, step=5):
    """
    Retrieves all values in a key's block (KEY, val1, val2, val3, val4).
    
    Args:
        result_array: The 1D array from parse_config_file()
        key_name: The key to search for
        step: Step size (default 5)
    
    Returns:
        Dictionary with indexed values, or None if not found
        
    Example:
        For key "c_btn20" at position 20:
        {
            "key": "c_btn20",
            "val1": "#3e3e42",
            "val2": "Color", 
            "val3": "4",
            "val4": "4"
        }
    """
    # Find the key position
    for i in range(0, len(result_array), step):
        if result_array[i] == key_name:
            # Extract the block
            block = {}
            block["key"] = result_array[i]
            
            for j in range(1, step):
                pos = i + j
                if pos < len(result_array):
                    block[f"val{j}"] = result_array[pos]
                else:
                    block[f"val{j}"] = ""
            
            return block
    
    return None  # Key not found


# --- Main Usage Example ---
if __name__ == '__main__':
    print("=== Parser with Getter Functions ===\n")
    
    # Parse the config file
    result_array = p2.parse_config_file()
    
    if not result_array:
        print("Error: No data parsed")
        exit(1)
    
    print(f"Parsed {len(result_array)} elements\n")
    
    # Example 1: Get value by key name
    print("--- Example 1: Get by Key Name ---")
    key1 = "c_btn20"
    val1 = get_by_key(result_array, key1)
    print(f'get_by_key("{key1}") = "{val1}"')
    
    key2 = "key_10__50__"
    val2 = get_by_key(result_array, key2)
    print(f'get_by_key("{key2}") = "{val2}"')
    
    # Example 2: Get value by direct index
    print("\n--- Example 2: Get by Direct Index ---")
    idx1 = 21
    val_idx1 = get_by_index(result_array, idx1)
    print(f"get_by_index({idx1}) = \"{val_idx1}\"")
    
    idx2 = 51
    val_idx2 = get_by_index(result_array, idx2)
    print(f"get_by_index({idx2}) = \"{val_idx2}\"")
    
    # Example 3: Get entire key block
    print("\n--- Example 3: Get Complete Key Block ---")
    block = get_key_block(result_array, "c_btn20")
    if block:
        print(f"Block for 'c_btn20':")
        for k, v in block.items():
            print(f"  {k}: \"{v}\"")
    
    # Write output file
    print("\n--- Writing Output File ---")
    p2.write_output_file(result_array)
    
    print("\n=== Finished ===")
