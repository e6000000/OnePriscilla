import os
import re  
# open Notepad++ ohne Dialog/Error-Handling
import subprocess
# compareFiles
import sys


# --- Globale Konfiguration ---
AI_ID = 2
SCRIPT_NAME = f"p{AI_ID}.py"
INFILE = "Gtst.htm"
OUTFILE = f"P{AI_ID}.htm"
OUTFILEPDAT = f"pDAT{AI_ID}.htm"


# Debug-Schalter. Setze auf True für detaillierte Ausgaben, sonst False.
DEBUG = True

# --- Konfiguration der Parser-Regeln ---
DELIMITERS = ['.', ',', '|', ';']
VALID_STEPS = {'step2': 2, 'step4': 4, 'step5': 5, 'step8': 8, 'step10': 10, 'step16': 16}
DEFAULT_STEP = 5

def parse_config_file():
    try:
        with open(INFILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"FEHLER: Eingabedatei '{INFILE}' nicht gefunden.")
        return []

    output_array = []
    step = DEFAULT_STEP
    step_is_finalized = False
    last_idx = -1
    delimiter_class = '[' + re.escape(''.join(DELIMITERS)) + ']'

    if DEBUG: print(f"--- Starte Verarbeitung von {INFILE} mit {len(lines)} Zeilen ---")

    for line_num, original_line in enumerate(lines):
        line = original_line.strip()
        if not line:
            continue

        if line.startswith('//'):
            pattern = r'^\/\/\s*\d+\s*' + delimiter_class
            if not re.match(pattern, line):
                if DEBUG: print(f"Zeile {line_num+1}: Ignoriert (reiner Kommentar). Inhalt: '{line}'")
                continue

        delimiter, d_pos = None, -1
        match = re.search(delimiter_class, line[:20])
        if match:
            delimiter = match.group(0)
            d_pos = match.start()
        else:
            if DEBUG: print(f"Zeile {line_num+1}: Übersprungen (kein Trennzeichen gefunden). Inhalt: '{line}'")
            continue

        head = line[:d_pos]
        content = line[d_pos + 1:]
        idx_str = "".join(filter(str.isdigit, head))

        if idx_str:
            idx = int(idx_str)
        else:
            idx = last_idx + 1
            if DEBUG: print(f"Zeile {line_num+1}: Keinen Index gefunden, generiere nächsten Index: {idx}")
        last_idx = idx

        if idx == 0 and not step_is_finalized:
            found_step_in_line = False
            for key, val in VALID_STEPS.items():
                if key in original_line:
                    step = val
                    print(f"Info: Step-Größe wurde aus Zeile {line_num+1} auf {step} gesetzt (Schlüsselwort '{key}' gefunden).")
                    found_step_in_line = True
                    break
            if not found_step_in_line and DEBUG:
                print(f"Warnung: In Zeile mit Index 0 wurde kein 'stepX' gefunden. Benutze Standard-Step: {step}.")
            step_is_finalized = True

        values = [p.strip() for p in content.split(delimiter)]

        if len(values) > step:
            if DEBUG: print(f"Zeile {line_num+1}: Kürze Werte von {len(values)} auf {step}.")
            values = values[:step]
        elif len(values) < step:
            values.extend([''] * (step - len(values)))

        start_pos = idx * step
        required_size = start_pos + step
        if len(output_array) < required_size:
            output_array.extend([''] * (required_size - len(output_array)))
        output_array[start_pos : start_pos + step] = values

        if DEBUG:
            print(f"Zeile {line_num+1}: Verarbeitet -> Index={idx}, Trennzeichen='{delimiter}', Werte={values} -> Positionen {start_pos}-{start_pos + step - 1}")

    # return output_array, step
    return output_array
    
'''
    # return output_array, step
    #        or 
    # return output_array


# **In your p2.py script, change the very last line of the parse_config_file function.
# **Change this:**  
# In p2.py, inside parse_config_file()
      return output_array

# **To this:**
# In p2.py, inside parse_config_file()
      return output_array, step


# ------------------------------------------------------------    
def parse_config_file():
    """
    Liest und verarbeitet die Konfigurationsdatei Gtst.htm und schreibt das Ergebnis
    in eine 1D-Array-Struktur in die Ausgabedatei G2.htm.
    
    Inklusive der Regel für die Behandlung von Kommentarzeilen.
    """ [T9](1)

def write_output_file(data):                  # in comment line
    """Schreibt das 1D-Array in die Zieldatei.""" [T12](2)
    
'''


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

def write_output_file(data):
    if not data:
        print("Warnung: Keine Daten zum Schreiben vorhanden.")
        return
    try:
        with open(OUTFILE, "w", encoding="utf-8") as f:
            # f.write(f"// Generated by {SCRIPT_NAME} (AI_ID: {AI_ID})  \n")
            # f.write(f"// Total elements: {len(data)} \n")
            for i, value in enumerate(data):
                f.write(f"{i} {value}\n")
        print(f"\n✓ ERFOLG: {len(data)} Elemente wurden in '{OUTFILE}' geschrieben.")
        
        # Nach write_output_file() oder am Ende von parse_config()
        subprocess.run(["notepad++", OUTFILE])
        # --- NEW LINE: Open the file with Notepad++ ---
        # os.system(f"notepad++.exe {OUTFILE}")
        
    except IOError as e:
        print(f"\nFEHLER: Schreiben der Datei '{OUTFILE}' fehlgeschlagen: {e}")

if __name__ == '__main__':
    print(f"--- Führe {SCRIPT_NAME} aus ---")
    if not os.path.exists(INFILE):
        print(f"Info: Eingabedatei '{INFILE}' nicht gefunden. Erstelle sie mit Testinhalt.")
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
            
    result_array = parse_config_file()
    #
    #   out result_array
    #
    write_output_file(result_array)
    print(f"--- {SCRIPT_NAME} beendet ---")
    
    # Nach write_output_file() oder am Ende von parse_config()
    subprocess.run(["notepad++", OUTFILE])
    # --- NEW LINE: Open the file with Notepad++ ---
    # os.system(f"notepad++.exe {OUTFILE}")

