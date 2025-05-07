a=[]
for i in range(1,101):
    if not i%7==0:
        a.append(i)
for i in range(0,len(a),10):
    print(a[i:i+10])