def n_super(n):
    if n==0:
        return 1
    else:
     k=1
     for i in range(1,n+1):
        k*=i
     return k

def sin_x(x,p):
    i=1
    f=10
    s=0
    while abs(f)>1e-5:
        f=((-1)**(i-1))*(x**(2*i-1))/(n_super(2*i-1))
        s+=f
        i+=1
    return s
print(sin_x(1,1e-5))