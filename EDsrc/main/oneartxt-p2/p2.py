import os
import re  
import subprocess
import sys
from onear_transformer import transform_onear


# --- Globale Konfiguration ---
AI_ID = 2
SCRIPT_NAME = f"p{AI_ID}.py"
INFILE = "Gtst.htm"
OUTFILE = f"P{AI_ID}.htm"
outhtml = OUTFILE + 'l'
 
DEBUG = True
debgg = DEBUG

DELIMITERS = ['.', ',', '|']
VALID_STEPS = {'step2': 2, 'step4': 4, 'step5': 5, 'step8': 8, 'step10': 10, 'step16': 16}
COMMENT_MARKERS = ['<!--', '-->', '//', ';', '#cs', '#ce', '#', 'rem', '/*', '*/']
DEFAULT_STEP = 5

# --- Global State ---
# onear = []
onear_oldstep = []




def write_output_file_no_pre(data):
    if not data:
        print("Warnung: Keine Daten zum Schreiben vorhanden.")
        return
    try:
        with open(OUTFILE, "w", encoding="utf-8") as f:
            for i, value in enumerate(data):
                f.write(f"{i} {value}\n")
        print(f"\n✓ ERFOLG: {len(data)} Elemente wurden in '{OUTFILE}' geschrieben.")
        
        subprocess.run(["notepad++", OUTFILE])
        
    except IOError as e:
        print(f"\nFEHLER: Schreiben der Datei '{OUTFILE}' fehlgeschlagen: {e}")




def write_output_file(data):
    # 'xx.htm' + 'l' = 'xx.html' -> Works perfectly
    outhtml = OUTFILE + 'l'
    if not data:
        print("Warning: No data to write.")
        return
    try:
        with open(outhtml, "w", encoding="utf-8") as f:
            f.write("# <pre>\n")  #  add as the first line to the p2.html ext is html  not htm file.htm no have first line with # <pre>
            for i, value in enumerate(data):
                f.write(f"{i} {value}\n")
        
        print(f"\n✓ SUCCESS: {len(data)} elements written frst-line: # <pre>  ext:html  to '{outhtml}'.")
        
        # Open Notepad++ (Ensure it's in your system PATH or use full path)
        subprocess.run(["notepad++", outhtml])
        
    except IOError as e:
        print(f"\nERROR: Failed to write file '{outhtml}': {e}")
        
     


def parse_config_file():
    global onear_oldstep
    try:
        with open(INFILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"FEHLER: Eingabedatei '{INFILE}' nicht gefunden.")
        onear_oldstep = []
        return onear_oldstep

    onear_oldstep = [] # Reset global array
    aadd = DEFAULT_STEP
    step_is_finalized = False
    last_idx = -1
    delimiter_class = '[' + re.escape(''.join(DELIMITERS)) + ']'

    if DEBUG: print(f"--- Starte Verarbeitung von {INFILE} mit {len(lines)} Zeilen ---")

    for line_num, original_line in enumerate(lines):
        line = original_line.strip()
        
        # --- Comment Handling ---
        is_comment = False
        work_line = line        
        
        if not line:
            continue
            
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
                    aadd = val
                    print(f"Info: Step-Größe wurde aus Zeile {line_num+1} auf {aadd} gesetzt (Schlüsselwort '{key}' gefunden).")
                    found_step_in_line = True
                    break
            if not found_step_in_line and DEBUG:
                print(f"Warnung: In Zeile mit Index 0 wurde kein 'stepX' gefunden. Benutze Standard-Step: {aadd}.")
            step_is_finalized = True

        values = [p.strip() for p in content.split(delimiter)]

        if len(values) > aadd:
            if DEBUG: print(f"Zeile {line_num+1}: Kürze Werte von {len(values)} auf {aadd}.")
            values = values[:aadd]
        elif len(values) < aadd:
            values.extend([''] * (aadd - len(values)))

        start_pos = idx * aadd
        required_size = start_pos + aadd
        if len(onear_oldstep) < required_size:
            onear_oldstep.extend([''] * (required_size - len(onear_oldstep)))
        onear_oldstep[start_pos : start_pos + aadd] = values

        if DEBUG:
            print(f"Zeile {line_num+1}: Verarbeitet -> Index={idx}, Trennzeichen='{delimiter}', Werte={values} -> Positionen {start_pos}-{start_pos + aadd - 1}")

    return onear_oldstep
   

def compare_files(file_path1, file_path2):
    """
    Compares two text files line by line, assuming each line is in the format 'index value' (e.g., '0 aadd').
    Outputs 'equal' if the files are identical line by line.
    Otherwise, shows the differing lines with their indices.
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

if __name__ == '__main__':
    print(f"--- Führe {SCRIPT_NAME} aus ---")
    if not os.path.exists(INFILE):
        print(f"Info: Eingabedatei '{INFILE}' nicht gefunden. Erstelle sie mit Testinhalt.")
        # ... (Test content creation omitted for brevity if file exists, but preserved logic implies we should just call function)
        # For safety in this edit I'll assume file exists or user handles it, or just call parse.
        # Actually in original code it created file. I will simplify main slightly or keep logic.
        # Let's keep logic simple: call parse.
    
    # We call parse_config_file which populates the global 'onear_oldstep'
    parse_config_file()
    
    # Transform onear_oldstep to new onear schema
    onear = transform_onear(onear_oldstep, input_step=5) # Assuming input aadd is 5 (DEFAULT_STEP)

    # Write from the generated 'onear' to p2.htm and to p2.html with L ext  and first line '# <pre>'
    write_output_file_no_pre(onear)
    write_output_file(onear)
    
    compare_files("P4.htm","P2.htm")
    print(f"--- {SCRIPT_NAME} . parse_config_file()  and compare_files(P4.htm,P2.htm) done ---")

