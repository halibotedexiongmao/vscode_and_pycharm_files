a=[]
b=[]
import random as r
for i in range (26):
    a.append(chr(ord('a')+i))
    a.append(chr(ord('A')+i))
for i in range(10):
    a.append(chr(ord('0')+i))
a.append('!')
a.append('@')
a.append('#')
a.append('%')
a.append('&')
a.append('*')
a.append('?')
print(a)
for i in range (8):
    b.append(a[r.randint(0,len(a))])
c="".join(b)
print(c)
