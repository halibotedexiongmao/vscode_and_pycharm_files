xs={'张三':90, '李四':80, '钱二':100}
a=list(xs.values())
b=max(a)
for i,j in xs.items():
    if b==j:
        c=i
        break
print("最高分是{},是{}".format(b,c))
print("平均分%s"%(sum(a)/len(a)))
name=input("请输入一名学生的姓名")
print(xs.get(name,"查无此人"))