import onear

print("--- TEST: onear.py Global State Access ---")

# 1. Setup Data
print("1. Initializing...")
onear.init(size=100)

# 2. Register Keys (Simulate what p4.py would do)
print("2. Registering Keys...")
onear.register_key("c_btn20", 22)
onear.register_key("my_val", 50)
onear.register_key("zero_val", 0)

# 3. Fill Data
print("3. Filling Data...")
onear.data[22] = "#FF0000"  # Value for c_btn20
onear.data[50] = "Hello World"
onear.data[0]  = "Start"

# 4. Test Access
print("\n--- Testing Access ---")

# A) oneindex()
idx_1 = onear.oneindex("c_btn20")
idx_2 = onear.oneindex(22)
idx_3 = onear.oneindex("22")

print(f"oneindex('c_btn20') -> {idx_1} (Expected 22)")
print(f"oneindex(22)        -> {idx_2} (Expected 22)")
print(f"oneindex('22')      -> {idx_3} (Expected 22)")

if idx_1 == idx_2 == idx_3 == 22:
    print("✓ INDEX LOOKUP WORKS")
else:
    print("X INDEX LOOKUP FAILED")

# B) onearkey()
val_1 = onear.onearkey("c_btn20")
val_2 = onear.onearkey(22)

print(f"\nonearkey('c_btn20') -> {val_1}")
print(f"onearkey(22)        -> {val_2}")

if val_1 == val_2 == "#FF0000":
    print("✓ VALUE ACCESS WORKS & IS IDENTICAL")
else:
    print("X VALUE ACCESS FAILED")

# C) Dictionary/Map Check (Simulate 'samesame')
a = onear.onearkey('c_btn20')
b = onear.data[22]

if a == b:
    print("\n✓ samesame ('key' == direct array access)")
else:
    print("\nX samesame FAILED")

print("\n--- TEST DONE ---")
