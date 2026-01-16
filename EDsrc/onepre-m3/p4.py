import os
# open Notepad++ ohne Dialog/Error-Handling
# later for notepad++ open: before: def create_test_file(): 
import subprocess
import sys    
import one_pre  # <--- Added import

    
# --- Global Configuration AI is Claude id 4 ---
AI_ID = 4
SCRIPT_NAME = f"p{AI_ID}.py"
INFILE = "Gtst.htm"
OUTFILE = f"P{AI_ID}.htm"
# Debug-Schalter. Setze auf True für detaillierte Ausgaben, sonst False.
DEBUG = True
DELIMITERS = ['.', ',', '|', ';']
VALID_STEPS = {'step2': 2, 'step4': 4, 'step5': 5, 'step8': 8, 'step10': 10, 'step16': 16}
COMMENT_MARKERS = ['<!--', '-->', '//', ';', '#cs', '#ce', '#', 'rem', '/*', '*/']         #   ';', '#cs', '#ce' is comment in autoit 
#   ';', '#cs', '#ce' is comment in autoit 
   
debgg = 1  # Debug mode: 1 = on, 0 = off


# --- Global State ---
onear = []

def parse_config():
    """
    Parses config file into 1D array structure (onear).
    """
    global onear
    
    # --- Initialization ---
    DELIMITERS = ['.', ',', '|', ';']
    VALID_STEPS = {'step2': 2, 'step4': 4, 'step5': 5, 'step8': 8, 'step10': 10, 'step16': 16}
    COMMENT_MARKERS = ['<!--', '-->', '//', ';', '#cs', '#ce', '#', 'rem', '/*', '*/']         #   ';', '#cs', '#ce' is comment in autoit 
    #   ';', '#cs', '#ce' is comment in autoit 
    
    try:
        with open(INFILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Input file '{INFILE}' not found.")
        onear = []
        return

    onear = [] # Reset Global Array
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

        if len(onear) < required_size:
            onear.extend([''] * (required_size - len(onear)))
        
        for i, value in enumerate(values):
            onear[start_pos + i] = value
        
        comment_flag = " [COMMENT]" if is_comment else ""
        if debgg:
            print(f"Line {line_num}{comment_flag}: idx={idx}, delim='{delimiter}', {len(values)} values → pos {start_pos}-{start_pos+step-1}")

    # --- Write Output ---
    try:
        with open(OUTFILE, "w", encoding="utf-8") as f:
            for i, value in enumerate(onear):
                f.write(f"{i} {value}\n")
        
        print(f"\n✓ SUCCESS: {len(onear)} elements written to '{OUTFILE}'")
        print(f"  Step size: {step}")
        print(f"  Debug mode: {'ON' if debgg else 'OFF'}")
        
    except IOError as e:
        print(f"ERROR: Write failed: {e}")


    # open Notepad++ ohne Dialog/Error-Handling
    # for notepad++ open: before: def create_test_file(): # import subprocess
    # Nach write_output_file() oder am Ende von parse_config()
    if debgg: subprocess.run(["notepad++", OUTFILE])
    # --- NEW LINE: Open the file with Notepad++ ---
    # os.system(f"notepad++.exe {OUTFILE}")


# --- OneSet / OneGet Wrappers ---
def oneset(q):
    """
    Example: oneset("Key Val Index Val")
    """
    one_pre.do_oneset(onear, q)

def oneget(q):
    """
    Example: oneget("Key Index") -> [Val1, Val2]
    """
    return one_pre.do_oneget(onear, q)


# -------------------------------------------------
# import sys
#
def compare_files(file_path1, file_path2):
    """
    Compares two text files line by line, assuming each line is in the format 'index value' (e.g., '0 step').
    Outputs 'equal' if the files are identical line by line.
    Otherwise, shows the differing lines with their indices.
    
    Args:
    file_path1 (str): Path to the first file.
    file_path2 (str): Path to the second file.
    
    Returns:
    None: Prints the comparison result to stdout.
    """
    try:
        with open(file_path1, 'r', encoding='utf-8') as f1:
            lines1 = [line.strip() for line in f1.readlines()]
        
        with open(file_path2, 'r', encoding='utf-8') as f2:
            lines2 = [line.strip() for line in f2.readlines()]
        
        if len(lines1) != len(lines2):
            print(f"Files have different lengths: {len(lines1)} vs {len(lines2)}")
            # Show all lines for brevity, but you can adjust
            for i, line in enumerate(lines1):
                if i < len(lines2):
                    if line != lines2[i]:
                        print(f"Line {i}: File1='{line}' != File2='{lines2[i]}'")
                else:
                    print(f"Extra line {i} in File1: '{line}'")
            for i in range(len(lines1), len(lines2)):
                print(f"Extra line {i} in File2: '{lines2[i]}'")
            return
        
        differences = []
        for i, (line1, line2) in enumerate(zip(lines1, lines2)):
            if line1 != line2:
                differences.append((i, line1, line2))
        
        if not differences:
            print("equal")
        else:
            print("Differences found:")
            for i, line1, line2 in differences:
                print(f"Line {i}: File1='{line1}' != File2='{line2}'")
                
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

'''
# Example usage:
# Assuming your files are named 'file1.txt' and 'file2.txt' with the provided content.
# compare_files('file1.txt', 'file2.txt')

# For your example data:
# If you save the first list to 'file1.txt':
# 0 step
# 1 step5
# 2 5
# 3 0
# 4 0
# 5 range_user5
# 6 31-99

# And the second to 'file2.txt':
# 0 step
# 1 step5
# 2 5
# 3 0
# 4 0
# 5 range_user_5__25
# 6 31-99

# Running compare_files('file1.txt', 'file2.txt') would output:
# Differences found:
# Line 5: File1='5 range_user5' != File2='5 range_user_5__25'

# -------------------------------------------
'''




# --- Test File Creator ---
def create_test_file():
    """Creates test input matching your configuration"""
    test_content = """
    
# <pre>
// ---  SAVED CONFIG   ---  0 | step5 | 5 | | | 
// lines mit (1)comment werden nur weiter geparst geprueft wenn : (2)index number direct nach (3)comment AND  dann (4)delimiter   AND  dann (5)key 
// kein index direct nach comment ignore line
// ID | not_valid_line_key     kein index direct nach comment ignore line
// ID   | KEY         | val1   | KEY2   | KEY3  |  KEY4 
// ID   | KEY         | val1   | val2   | val3  |  val4 
0 | step | step5      |  5     |0       |0      |0|0|0|    easy: 0,step ,step5 ,,,,
-->1     | range_user_1_arr_5 | 31-99  |1       |1      |1  | 1 | <!--      
<!--2    , c_bg_2_array_10       ,#320a2b ,Color    , 2    ,2,2,2,2,2,
-->3     | dbgg       | 1      | c_fg    | #cccccc | Color  | 3  |3 | 3 | 3 | 3  | | | | 5 comment /***/
/* 4.      c_btn_4_ar_20      .#3e3e42 .Color    . 4    .4.4.4.4.4.4.4.
,key_ohne_index ohne comment25 , Segoe UI , Font , -   , index 5*5= 25 wird fuer key_ohne_index  berechnet    comment /***/
# 6.key6_ar_30  .6.6.6.6.6.6.6.6.....
//,key7,,,7,7,,,7,7,7,,,    must ignore , kein index   direct nach comment
  ,key8 , ,7  ,7,7,7,7,,,,    ok index next(6+1)*5 fuer key8 is number t weil 7 wurde comment wird berechnet
  10 . key_10_array_50_ . value_key_10   . key_10_2_value_10_2  . key_10_3_value_10_3 .  key_10_4_value_10_4 . "key_10_5_value_10_5   10_5 not used"

"""
    test_out = """
0 step
1 step5
2 5
3 0
4 0
5 range_user5
6 31-99
7 1
8 1
9 1
10 c_bg_10
11 #320a2b
12 Color
13 2
14 2
15 dbgg15
16 1
17 c_fg
18 #cccccc
19 Color
20 c_btn20
21 #3e3e42
22 Color
23 4
24 4
25 key_ohne_index ohne comment25
26 Segoe UI
27 Font
28 -
29 index 5*5= 25 wird fuer key berechnet    comment /***/
30 key6__30__
31 6
32 6
33 6
34 6
35 key8__35__
36 
37 7
38 7
39 7
40 
41 
42 
43 
44 
45 
46 
47 
48 
49 
50 key_10__50__
51 value_key_10
52 key_10_2_value_10_2
53 key_10_3_value_10_3
54 key_10_4_value_10_4
    
 
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
    
    # write_output_file(result_array)
    compare_files("P4.htm","P2.htm")
    print(f"--- {SCRIPT_NAME} . parse_config()  and compare_files(P4.htm,P2.htm) done ---")

