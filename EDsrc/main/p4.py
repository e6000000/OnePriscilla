import os

# --- Global Configuration AI is Claude id 4 ---
AI_ID = 4
SCRIPT_NAME = f"p{AI_ID}.py"
INFILE = "Gtst.htm"
OUTFILE = f"P{AI_ID}.htm"

debgg = 1  # Debug mode: 1 = on, 0 = off


def parse_config():
    """
    Parses config file into 1D array structure.
    
    Rules:
    1. Search for "stepX" keyword to determine step size
    2. Index 0 is treated like any other index (no special handling)
    3. Key name before delimiter can be anything
    4. Comment lines: Only parse if index number DIRECTLY after comment opener
       Examples:
       - <!--2-->|key|value  → VALID (index 2 directly after <!--)
       - //7,key,value       → INVALID (no index directly after //)
       - -->1|key|value      → VALID (index 1 directly after -->)
    """
    # --- Initialization ---
    DELIMITERS = ['.', ',', '|', ';']
    VALID_STEPS = {'step2': 2, 'step4': 4, 'step5': 5, 'step8': 8, 'step10': 10, 'step16': 16}
    COMMENT_MARKERS = ['<!--', '-->', '//', '/*', '*/']
    
    try:
        with open(INFILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Input file '{INFILE}' not found.")
        return

    out_arr = []
    step = 5  # Default
    step_found = False
    last_idx = -1

    print(f"--- Processing {len(lines)} lines ---")

    # --- Main Loop ---
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        if not line:
            continue

        # --- Comment Handling ---
        is_comment = False
        work_line = line
        
        # Check for any comment marker at start
        for marker in COMMENT_MARKERS:
            if line.startswith(marker):
                is_comment = True
                # Remove comment marker
                work_line = line[len(marker):].strip()
                
                # Check if index number is DIRECTLY after comment marker
                if not work_line or not work_line[0].isdigit():
                    if debgg:
                        print(f"Line {line_num}: Skipped (comment '{marker}' without direct index number)")
                    work_line = None
                    break
                
                if debgg:
                    print(f"Line {line_num}: Valid comment with '{marker}' + index")
                break
        
        # Skip if comment was invalid
        if work_line is None:
            continue

        # Find first delimiter
        d_pos = -1
        delimiter = None
        for i, char in enumerate(work_line[:20]):
            if char in DELIMITERS:
                d_pos = i
                delimiter = char
                break
        
        if d_pos == -1:
            if debgg:
                print(f"Line {line_num}: Skipped (no delimiter)")
            continue

        head = work_line[:d_pos]
        content_str = work_line[d_pos + 1:]
        
        # --- Parse Index ---
        idx_digits = "".join(filter(str.isdigit, head))
        
        if idx_digits:
            idx = int(idx_digits)
        else:
            idx = last_idx + 1
            if debgg:
                print(f"Line {line_num}: Generated index {idx}")
        
        last_idx = idx

        # --- Step Size Detection: Search for "stepX" keyword ---
        if not step_found:
            line_lower = line.lower()
            for step_keyword, step_value in VALID_STEPS.items():
                if step_keyword in line_lower:
                    step = step_value
                    step_found = True
                    print(f"INFO: Step size set to {step} (found '{step_keyword}' in line {line_num})")
                    break

        # --- Parse Values ---
        values = [v.strip() for v in content_str.split(delimiter)]
        
        # Remove empty trailing values
        while len(values) > 0 and values[-1] == '':
            values.pop()

        # --- Normalize to Step Size ---
        if len(values) > step:
            if debgg:
                print(f"Line {line_num}: Truncating {len(values)} to {step}")
            values = values[:step]
        elif len(values) < step:
            values.extend([''] * (step - len(values)))

        # --- Insert into 1D Array ---
        start_pos = idx * step
        required_size = start_pos + step

        if len(out_arr) < required_size:
            out_arr.extend([''] * (required_size - len(out_arr)))
        
        for i, value in enumerate(values):
            out_arr[start_pos + i] = value
        
        comment_flag = " [COMMENT]" if is_comment else ""
        if debgg:
            print(f"Line {line_num}{comment_flag}: idx={idx}, delim='{delimiter}', {len(values)} values → pos {start_pos}-{start_pos+step-1}")

    # --- Write Output ---
    try:
        with open(OUTFILE, "w", encoding="utf-8") as f:
            for i, value in enumerate(out_arr):
                f.write(f"{i} {value}\n")
        
        print(f"\n✓ SUCCESS: {len(out_arr)} elements written to '{OUTFILE}'")
        print(f"  Step size: {step}")
        print(f"  Debug mode: {'ON' if debgg else 'OFF'}")
        
    except IOError as e:
        print(f"ERROR: Write failed: {e}")


# --- Test File Creator ---
def create_test_file():
    """Creates test input matching your configuration"""
    test_content = """0 | step | step5      |  5     |0       |0      |0|0|0|
-->1     | range_user | 31-99  |1       |1      |1  | 1 |
<!--2    , c_bg       ,#320a2b ,Color    , 2    ,2,2,2,2,2,
-->3     | dbgg       | 1      | c_fg    | #cccccc | Color  | 3  |3 | 3 | 3 | 3  | | | | 5 comment /*
/**/4.      c_btn      .#3e3e42 .Color    . 4    .4.4.4.4.4.4.4.
,key_ohne_index ohne comment, Segoe UI , Font , -   , index 5*5= 25 wird fuer key berechnet 
; 6.key6  .6.6.6.6.6.6.6.6.....
//,key7,,,7,7,,,7,7,7,,,
  ,key8 , ,8  ,8,8,8,8,,,,
 10 . key_10 . value_key_10   . key_10_2_value_10_2  . key_10_3_value_10_3 .  key_10_4_value_10_4 . "key_10_5_value_10_5   10_5 not used"
"""
    
    with open(INFILE, "w", encoding="utf-8") as f:
        f.write(test_content)
    print(f"Test file '{INFILE}' created with your configuration")


# --- Main ---
if __name__ == '__main__':
    print(f"--- Running {SCRIPT_NAME} (AI_ID={AI_ID}) ---")
    
    if not os.path.exists(INFILE):
        print(f"Creating test file...")
        create_test_file()
    
    parse_config()
    print("--- Finished ---")
