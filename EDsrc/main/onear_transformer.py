
def transform_onear(onear_old, input_step=5):
    """
    Transforms the linear array 'onear_old' (based on input_step, default 5)
    into a new expanded array with double the step size (10).
    
    Transformation Rule:
    Old Block (Indices 0-4 relative to block start):
    0: Key
    1: Val1
    2: Val2
    3: Val3
    4: Val4
    
    New Block (Indices 0-9 relative to block start):
    0: Key (Old 0)
    1: Val1 (Old 1)
    2: Key + "1"
    3: Val2 (Old 2)
    4: Key + "2"
    5: Val3 (Old 3)
    6: Key + "3"
    7: Val4 (Old 4)
    8: Key + "4"
    9: Empty ("")
    """
    
    new_step = input_step * 2
    
    # Calculate how many full blocks we have
    # If onear_old length is not a multiple of input_step, we might need to pad or handle it.
    # Assuming p2.py ensures padding or we strictly process chunks.
    
    # We'll stick to a list comprehension or loop for clarity.
    onear_new = []
    
    # Iterate through chunks
    num_blocks = (len(onear_old) + input_step - 1) // input_step
    
    for i in range(num_blocks):
        base_idx = i * input_step
        chunk = onear_old[base_idx : base_idx + input_step]
        
        # Pad chunk if it's shorter than input_step (just in case)
        if len(chunk) < input_step:
            chunk.extend([''] * (input_step - len(chunk)))
            
        key = str(chunk[0])
        val1 = chunk[1]
        val2 = chunk[2]
        val3 = chunk[3]
        val4 = chunk[4]
        
        new_block = [''] * new_step
        
        # 0: Key
        new_block[0] = key
        # 1: Val1
        new_block[1] = val1
        
        # 2: Key + "1"
        new_block[2] = key + "1" # User requested: 'keyname' + '1'
        # 3: Val2
        new_block[3] = val2
        
        # 4: Key + "2"
        new_block[4] = key + "2"
        # 5: Val3
        new_block[5] = val3
        
        # 6: Key + "3"
        new_block[6] = key + "3"
        # 7: Val4
        new_block[7] = val4
        
        # 8: Key + "4"
        new_block[8] = key + "4"
        
        # 9: Empty
        new_block[9] = ""
        
        onear_new.extend(new_block)
        
    return onear_new
