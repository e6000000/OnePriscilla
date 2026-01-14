import p4

# Ensure config is parsed
p4.parse_config()

# local l3  l4 l5 l6 

onget  l5  20    l6  25  
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen

l3 = p4.onear[20 if 20 < len(p4.onear) else 0]
l4 = p4.onear[25 if 25 < len(p4.onear) else 0]

## print(f" l5={c_btn20}      l6={dbgg15}    ")
print(f" l5={l5}      l6={l6}    ")
