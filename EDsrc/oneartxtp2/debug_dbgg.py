import p4

print("Parsing config...")
p4.parse_config()

print(f"Size of onear: {len(p4.onear)}")

try:
    idx = p4.onear.index('dbgg')
    print(f"FOUND 'dbgg' at index {idx}")
    print(f"Value at {idx}: '{p4.onear[idx]}'")
except ValueError:
    print("ERROR: 'dbgg' NOT FOUND in onear.")
    print("Dumping indices 10 to 20:")
    for i in range(10, 21):
        if i < len(p4.onear):
            print(f"  {i}: '{p4.onear[i]}'")
