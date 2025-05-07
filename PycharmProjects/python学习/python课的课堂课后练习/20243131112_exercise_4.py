a=input("请输入一段含有z的字符串：")
c=list(a)
b=False
for i in a:
    if ord(i)==ord('z'):
        b=True
        break
if b:
    start=0
    for i in range(len(a)):
          if ord(a[i])>ord('a') and ord(a[i])<ord('z'):
             if ord(a[i])==ord('z'):
                 c[i]=('a')
             else:
                c[i]=chr(ord(a[i])+1)
    print(''.join(c))

else:
    print("请重新输入")
