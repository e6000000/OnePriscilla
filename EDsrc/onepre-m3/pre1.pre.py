import p4
from p4 import onear

# local  l1  l2  l3  l4  l5  l6



#  c_btn20   #3e3e4211   c_bg_10   #320a2b11
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen
p4.oneset("c_btn20   #3e3e4211   c_bg_10   #320a2b11")

# c_btn20   #3e3e4222   c_bg_10   #320a2b22
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen
p4.oneset("c_btn20   #3e3e4222   c_bg_10   #320a2b22")


l1, l2 = p4.oneget("dbgg15 Color")
# hier muesste nach one_pre.py scan strRepl dann py syntax stehen

# das braucht wohl noch eine func:  onear[dbgg15]
# Note: dbgg15 must be an integer variable for this to work in Python!
print(f" c_btn20={onear[15]}      c_bg_10={onear[Color]}    ")
# print  c_btn20 =   c_bg_10  =  // schreib correcte syntax please
# print(f" l1={dbgg15}      l2={Color}    ")
