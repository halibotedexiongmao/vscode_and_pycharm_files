#2025.04.29 writen by qbluan for digital economic
import numpy as np
import copy
#import matplotlib as plt
#======= 说明 =======#
#多属性，单标签线性回归问题
#属性：X=(1x,2x,3x,...,Nx)，n+1行N列，其中Ix表示第I个样本的属性，I=1,2,...,N。
#Ix为列向量Ix=(Ix1,Ix2,...,Ixn,1)^T，n+1行1列，其中Ixj为第I个样本的第j个属性，j=1,2,...,n。
#Y=(1y,2y,...,Ny)，1行N列，其中Iy表示第I个样本的标签，I=1,2,...,N。
#W=(w1,w2,...,wn,b)^T为权重的列向量，n+1行1列
#损失函数:L=(Y-W^TX)(Y-W^TX)^T
#优化问题：W*=argmin[L(W)]
#闭式解：W*=(XX^T)^-1@X@Y^T
#梯度下降法：W[k+1]=W[k]-a*grad[w]L=W[k]+a*X(Y-W^TX)^T，其中W[k]表示第k次迭代的权重W
#======= 参数赋值 =========#
sol_type=1 # =0闭式解；=1梯度下降法
dataset_type=0 #=0随机生成；=1直接赋值；=2从文件读取
#------- 构造数据集参数 ------#
data_dim=2 #属性的数目
data_num=3 #样例的数目
#dataset_type=0的参数
#随机斜率范围[ks,kl]
ks=10
kl=11
#属性随机范围[xs,xl]
xs=0.
xl=1.
#dataset_type=1的参数
x0=[2,5,6,12]
y0=[4,9,13,22]
#dataset_type=2的参数
docadd=''#数据集文件的地址
docname=''#数据集文件的名字

#------- 梯度下降参数 ------#
#sol_type=1
#初始随机权重范围[ws,wl]
ws=0.1
wl=1.
iter_max=20000 #最大迭代步数
lr=0.1 #学习率
parastop=0.001
jstep=10
contype=0#=0，根据残差判断收敛；=10，预留，根据相对权重变化判断收敛
#=========================#

if dataset_type==2:
    docinf=docadd+docname

if dataset_type==0:
    ddimp=data_dim+1
    ddimm=data_dim-1
    x=np.zeros((ddimp,data_num))
    y=np.zeros((1,data_num))
    k=np.random.uniform(ks,kl,ddimp)
    print('k=',k)
    for i in range(data_num):
        x[0:data_dim,i]=np.random.uniform(xs,xl,data_dim)
        x[data_dim, i]=1.
    y=k.dot(x)


if sol_type == 0:
    temp=x@x.T
    tempinv=np.linalg.inv(temp) #伪逆
    w=tempinv@x@(y.T)
    print(w)
print('=============')


if sol_type == 1:
    w=np.random.uniform(ws,wl,ddimp)
    w.reshape(ddimp,1)
    for j in range(iter_max):
         tempy = w.T @ x - y
         tempyT=tempy.T
         gradl=2*x@tempyT
         tempw=w-lr*gradl
         Loss=tempy@tempyT
         if contype==0:
             elystp=Loss
         if contype==1:
             elystp=Loss/(y@y.T)
         if j % jstep == 0:
             print('j=', j)
             print('损失函数：', elystp)
         w = tempw
         if elystp < parastop:
             break

    if j==iter_max:
        print('not convergent,try again!')
    if j<iter_max:
        print('=====================================================')
        print('j=', j)
        print('w=',w)
        print('损失函数：', elystp)












