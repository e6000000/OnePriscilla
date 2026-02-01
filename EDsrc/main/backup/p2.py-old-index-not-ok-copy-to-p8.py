
# AI: gemini (ID 2)
# 2 okokok   ---idxq_3106---2026_01_12---10_56_31
# Command to run: py -3.10 p2.py

import os

# --- Global Configuration based on AI Naming Scheme ---
AI_ID = 2
SCRIPT_NAME = f"p{AI_ID}.py"
INFILE = "Gtst.htm"
OUTFILE = f"G{AI_ID}.htm"

def parse_config():
    """
    Parses a config file using a robust method to handle complex line formats.

    The logic finds the first delimiter in a line's first 10 chars. It then
    extracts only digits before the delimiter as the index. This correctly
    ignores any comment-like characters (e.g., '-->', '//') without needing
    a predefined list of comment markers.
    """
    # --- 1. Initialization ---
    DELIMITERS = ['.', ',', '|']
    VALID_STEPS = {'step2': 2, 'step4': 4, 'step5': 5, 'step8': 8, 'step10': 10, 'step16': 16}
    
    try:
        with open(INFILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Input file '{INFILE}' not found.")
        return

    out_arr = []
    step = 5  # Default step size
    step_found = False
    last_idx = -1

    # --- 2. Main Processing Loop ---
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Find the first delimiter within the first 10 characters
        d_pos = -1
        for i, char in enumerate(line[:10]):
            if char in DELIMITERS:
                d_pos = i
                break
        
        if d_pos == -1:
            continue # Ignore lines without a delimiter in the head

        delimiter = line[d_pos]
        head = line[:d_pos]
        
        # --- 3. Parse Index (Robust Method) ---
        # Extract only digits from the part before the delimiter.
        # This correctly ignores all comment characters like '-->', '///', '<!--'.
        idx_digits = "".join(filter(str.isdigit, head))
        
        if idx_digits:
            idx = int(idx_digits)
        else:
            idx = last_idx + 1
        last_idx = idx

        # --- 4. Detect Step Size from Line 0 (as per rule 7) ---
        if not step_found and idx == 0:
            for key, val in VALID_STEPS.items():
                if key in line:
                    step = val
                    step_found = True
                    print(f"Info: Step size set to {step} from line 0.")
                    break
            # Mark as found to prevent re-checking on malformed files
            step_found = True

        # --- 5. Parse Values ---
        # Values are everything *after* the first delimiter
        content_str = line[d_pos + 1:]
        values = [p.strip() for p in content_str.split(delimiter)]

        # --- 6. Normalize Value Block and Insert into Array ---
        # Truncate if there are too many values, or pad if too few
        if len(values) > step:
            values = values[:step]
        else:
            values.extend([''] * (step - len(values)))
            
        start_pos = idx * step
        required_size = start_pos + step

        # Extend output array if it's not large enough
        if len(out_arr) < required_size:
            out_arr.extend([''] * (required_size - len(out_arr)))
        
        # Place the block of values into the array
        out_arr[start_pos : start_pos + step] = values

    # --- 7. Write to Output File ---
    try:
        with open(OUTFILE, "w", encoding="utf-8") as f:
            for i, v in enumerate(out_arr):
                f.write(f"{i} {v}\n")
        print(f"Success: Wrote {len(out_arr)} items to '{OUTFILE}'.")
    except IOError as e:
        print(f"ERROR: Failed to write to file '{OUTFILE}': {e}")

# --- Main execution block ---
if __name__ == '__main__':
    print(f"--- Running Parser ({SCRIPT_NAME}) ---")
    if os.path.exists(INFILE):
        parse_config()
    else:
        print(f"ERROR: Input file '{INFILE}' does not exist. Please create it.")
    print("--- Parser Finished ---")
