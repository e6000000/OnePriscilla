import p4

# Ensure config is parsed
p4.parse_config()

# local  l1  l2  l3  l4  l5  l6

oneset  c_btn20   #3e3e4211   c_bg_10   #320a2b11 
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen
oneset   c_btn20   #3e3e4222   c_bg_10   #320a2b22
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen
onget  l1 dbgg15   l2   Color 
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen

# das braucht wohl noch eine func:  onear[dbgg15]
# print(f" c_btn20={onear[dbgg15]}      c_bg_10={onear[Color]}    ")
# print  c_btn20 =   c_bg_10  =  // schreib correcte syntax please
print(f" l1={l1}      l2={l2}    ")
