import shlex
import os
import re

# --- Runtime Logic (for do_oneset/get) ---

def do_oneset(onear_list, query_string):
    """
    Parses 'Key1 Val1 Key2 Val2' or 'Index1 Val1' and updates onear_list.
    """
    if not query_string:
        return

    try:
        # Enable comments=False so #333 colors are not stripped
        tokens = shlex.split(query_string, comments=False)
    except Exception as e:
        print(f"ONESET ERROR: Parse error '{e}'")
        return

    # Process in pairs
    for i in range(0, len(tokens), 2):
        if i + 1 >= len(tokens):
            print(f"ONESET WARNING: Missing value for key '{tokens[i]}'")
            break
            
        key_or_idx = tokens[i]
        val = tokens[i+1]
        
        target_idx = -1
        
        # 1. Try Integer Index (Logical Index)
        if key_or_idx.isdigit():
            target_idx = int(key_or_idx)
        else:
            # 2. Search for Key
            try:
                found_at = onear_list.index(key_or_idx)
                target_idx = found_at
            except ValueError:
                # Fallback: Try stripped keys if exact match fails
                # (User reported 'dbgg' fail, maybe it has spaces in array?)
                found = False
                for idx, item in enumerate(onear_list):
                    if str(item).strip() == key_or_idx:
                        target_idx = idx
                        found = True
                        break
                if not found:
                    print(f"ONESET ERROR: Key '{key_or_idx}' not found.")
                    continue
        
        # Perform Update (at target + 1)
        write_pos = target_idx + 1
        
        if write_pos < len(onear_list):
            onear_list[write_pos] = val
            print(f"oneset: Updated [{write_pos}] = '{val}' (via '{key_or_idx}')")
        else:
            print(f"ONESET ERROR: Index {write_pos} out of bounds.")


def do_oneget(onear_list, query_string):
    """
    Parses 'Key Index Key' and returns list of values.
    """
    if not query_string:
        return []

    try:
        # Enable comments=False so #333 colors are not stripped
        tokens = shlex.split(query_string, comments=False)
    except Exception as e:
        print(f"ONEGET ERROR: Parse error '{e}'")
        return []

    results = []
    
    for item in tokens:
        read_idx = -1
        
        if item.isdigit():
             read_idx = int(item)
        else:
            try:
                read_idx = onear_list.index(item)
            except ValueError:
                # Fallback: Try stripped keys
                found = False
                for idx, x in enumerate(onear_list):
                    if str(x).strip() == item:
                        read_idx = idx
                        found = True
                        break
                
                if not found:
                    print(f"ONEGET ERROR: Key '{item}' not found.")
                    results.append(None)
                    continue
        
        # Get Value at Index + 1
        val_idx = read_idx + 1
        if val_idx < len(onear_list):
            val = onear_list[val_idx]
            results.append(val)
        else:
            results.append(None)
            
    return results


# --- Preprocessor Logic ---

def run_preprocessor():
    # Resolve valid path to list file (relative to this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    list_file = os.path.join(script_dir, "one_pre_list.txt")
    
    if not os.path.exists(list_file):
        print(f"PREPROCESSOR: Config file '{list_file}' not found.")
        return

    with open(list_file, 'r') as f:
        # Read filenames and resolve them relative to script dir too
        files_to_scan = []
        for line in f:
            clean = line.strip()
            if clean and not clean.startswith("#"):
                # Assume listed files are in the same folder as the script
                files_to_scan.append(os.path.join(script_dir, clean))

    print(f"PREPROCESSOR: Scanning {len(files_to_scan)} files...")

    for fname in files_to_scan:
        if not os.path.exists(fname):
            print(f"  - Warning: File '{fname}' not found.")
            continue
        
        print(f"  -> Processing '{fname}'")
        process_file(fname)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    modified = False

    for line in lines:
        stripped = line.strip()
        
        # Detect 'oneset' at start of line
        if stripped.startswith("oneset ") or stripped.startswith("oneset\t"):
            # Syntax: oneset Key Val Key Val
            # Goal: p4.oneset("Key Val Key Val")
            
            # Extract arguments
            parts = line.split("oneset", 1) # Split only on first occurrence
            indentation = parts[0]
            args_comment = parts[1].strip()
            
            # IMPORTANT: Do NOT split on '#' here. Logic:
            # We treat the ENTIRE rest of the line as the string argument.
            # Why? Because colors like #aabbcc start with # but are valid values.
            # If the user wants real comments at the end, they will be passed 
            # into the string and oneset() runtime must deal with them (or ignore/error).
            # But currently safest is: Pass EVERYTHING.
            
            # Check if strictly ending with a comment? Hard to know user intent 100%.
            # But given the requirement "keine lust tippen", usually simplicity rules.
            # We wrap the whole text in quotes.
            
            py_code = f"{indentation}p4.oneset(\"{args_comment}\")\n"
            new_lines.append(py_code)
            modified = True
            
        # Detect 'oneget' or 'onget'
        elif stripped.startswith("oneget ") or stripped.startswith("onget "):
            cmd = "oneget" if stripped.startswith("oneget") else "onget"
            
            parts = line.split(cmd, 1)
            indentation = parts[0]
            raw_args = parts[1].strip()
            
            # Do NOT split on '#' here either.
            clean_args = raw_args
            
            try:
                tokens = clean_args.split() # Split by whitespace
                if len(tokens) % 2 != 0:
                    print(f"    ERROR in line: '{stripped}'. Arguments not in pairs (Var Key).")
                    new_lines.append(line) # Keep original if error
                    continue
                
                vars_list = []
                keys_list = []
                
                for i in range(0, len(tokens), 2):
                    vars_list.append(tokens[i])
                    keys_list.append(tokens[i+1])
                
                # Construct Python Code
                # l1, l2 = p4.oneget("dbgg15 Color")
                lhs = ", ".join(vars_list)
                rhs_keys = " ".join(keys_list)
                
                py_code = f"{indentation}{lhs} = p4.oneget(\"{rhs_keys}\")\n"
                new_lines.append(py_code)
                modified = True
                
            except Exception as e:
                print(f"    ERROR parsing line '{stripped}': {e}")
                new_lines.append(line)
                
        else:
            new_lines.append(line)

    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"    ✓ Updated '{filepath}'")
        except Exception as e:
            print(f"    ERROR writing file: {e}")
    else:
        print(f"    (No changes)")

if __name__ == "__main__":
    # If run directly, assume Preprocessor Mode requested via 'run_preprocessor' or CLI args?
    # User said execution via 'py one_pre.py'.
    # But usually this file is imported by p4.py. 
    # If imported, __name__ != __main__.
    # If run directly as script, run preprocessor.
    run_preprocessor()
