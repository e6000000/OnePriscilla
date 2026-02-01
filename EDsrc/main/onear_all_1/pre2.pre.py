import p4
from p4 import onear

# local l3  l4 l5 l6 

l5, l6 = p4.oneget("20 25")
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen

# Assumes l3, l4 are locals or intents to invoke something
l3 = onear[20] if 20 < len(onear) else None
l4 = onear[25] if 25 < len(onear) else None

## print(f" l5={c_btn20}      l6={dbgg15}    ")
print(f" l5={l5}      l6={l6}    ")
