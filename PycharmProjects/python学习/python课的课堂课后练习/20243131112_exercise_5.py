def compute_a(a,n):
    s=0
    for i in range (1,n+1):
        s+=int(str(a)*i)
    return "该值为：{}".format(s)

print(compute_a(2,5))