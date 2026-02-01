import p4
# file  test_setget_basic.py    # IMMER! reinschreiben aber immer alles english :-) 
print("--- TEST 1: Basic Index Access ---")

# 1. Init
print("Initializing config...")
p4.parse_config()

# 2. Check variables we plan to change
# 10 c_bg_10 -> Value at 11 is #320a2b
# 15 dbgg15  -> Value at 16 is 1
initial_vals = p4.oneget("10 15")
print(f"Initial Values (10, 15): {initial_vals}")

# 3. SET via Index/Key-Combo string
# Note: In our current implementation '10' is treated as Key-Index. 
# We update the Value at idx+1 (so 11 and 16).
print("Executing: oneset '10 #NEWCOLOR 15 0'")
p4.oneset("10 #NEWCOLOR 15 0")

# 4. GET and Verify
new_vals = p4.oneget("10 15")
print(f"New Values (10, 15):     {new_vals}")

if new_vals == ['#NEWCOLOR', '0']:
    print("SUCCESS: Values updated correctly.")
else:
    print("FAILURE: Values mismatch.")
    
''' out  
Initial Values (10, 15): ['#320a2b', '1']
Executing: oneset '10 #NEWCOLOR 15 0'
oneset: Updated [11] = '#NEWCOLOR' (via '10')
oneset: Updated [16] = '0' (via '15')
New Values (10, 15):     ['#NEWCOLOR', '0']
SUCCESS: Values updated correctly.    
'''



## ------------------------------------------------------