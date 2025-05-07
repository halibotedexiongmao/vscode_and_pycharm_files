a=input("请输入一段字符串：")
b=list(set(a))
c={}
for i in b:
    c[i]=a.count(i)
print(c)