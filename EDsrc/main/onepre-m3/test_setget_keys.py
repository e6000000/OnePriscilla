import p4
# file  test_setget_keys.py    # IMMER! reinschreiben aber immer alles english :-) 
print("--- TEST 2: Key Access & Strings ---")

# 1. Init
p4.parse_config()

# 2. Check c_fg
print("Initial c_fg:", p4.oneget("c_fg"))

# 3. SET via Key
print("Executing: oneset c_fg '#FF00FF'")
p4.oneset("c_fg '#FF00FF'")

# 4. Strings with spaces
print("Executing: oneset dbgg 'Hello Space World'")
p4.oneset("dbgg 'Hello Space World'")

# 5. Verify
vals = p4.oneget("c_fg dbgg")
print(f"Result: {vals}")

if vals[0] == '#FF00FF' and vals[1] == 'Hello Space World':
    print("SUCCESS: Keys and Quoted Strings work.")
else:
    print("FAILURE.")

''' out
Initial c_fg: ['#cccccc']
Executing: oneset c_fg '#FF00FF'
oneset: Updated [18] = '#FF00FF' (via 'c_fg')
Executing: oneset dbgg 'Hello Space World'
ONESET ERROR: Key 'dbgg' not found.
ONEGET ERROR: Key 'dbgg' not found.
Result: ['#FF00FF', None]
FAILURE.


'''

## ------------------------------------------------------