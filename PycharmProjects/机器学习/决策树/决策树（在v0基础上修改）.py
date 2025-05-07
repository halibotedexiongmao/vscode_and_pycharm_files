#case3
#     --------------- 属性 --------------    标签
#编号 色泽   根蒂   敲声   纹理   脐部   触感    好瓜
# 1  青绿1  蜷缩1  浊响1  清晰1  凹陷1  硬滑1    是1
# 2  乌黑2    1   沉闷2    1     1      1      1
# 3    2     1     1      1     1      1      1
# 4    1     1     2     1     1      1       1
# 5    3     1     1     1     1      1       1
# 6    1   稍蜷2    1     1    稍凹2  软粘2     1
# 7    2     2     1    稍糊2   2      2       1
# 8    2     2     1     1     2      1       1
# 9    2     2     2     2     2      1       0
#10    1   硬挺3  清脆3    1    平坦3   2       0
#11    3     3     3     3     3      1       0
#12    3     1     1     3     3      2       0
#13    1     2     1     2     1      1       0
#14  浅白3    2     2     2     1      1       0
#15    2     2     1     1     2      2       0
#16    3     1     1    模糊3   3      1       0
#17    1     1     2      2    2      1       0
import numpy as np
import math
#import pandas as pd

def comS(karr,T):
#comS为计算样本的信息熵函数，形参中karr为各类别出现次数的列表，T为样例总数
#如一个样本中若出现0类的次数为a0，1类为a1，2类为a2，则karr=[a1,a2,a3],T=a1+a2+a3
#参数T允许小于等于0，样例总数通过计算得到。
#- 对应信息熵,
    L=len(karr)
    Sum=sum(karr)
    if T>0:
        if Sum!=T:
            print("error:check input information of function of comS")
            exit()
    if T<=0:
        T=Sum

    S=0
    for i in range(L):
        if karr[i]==0:
            continue
        pi=karr[i]/T
        S=S-pi*math.log2(pi)
    return S


def comSD(floorchar,Dfig_char,Darr,D,diaflag):
    #comSD计算按某一属性划分的信息增益
    #D为样本中样例总数，若D<=0,D通过Darr中的数据计算
    #floorchar为属性名字的字符串，Dfig_char为属性具体取值的字符串，Darr为不同属性取值
    #不同类别个数的列表，如某N个样例的样本有两个类别，某属性有两个取值，其中一个取值对应的
    #两个类别数目分别为m1和N-m1，另一个取值为m2和N-m2，则Darr=[[m1,N-m1],[m2,N-m2]]。
    #D为当前样本总数。diaflag为输出
    #对话的控制参数。
    #属性个数取值的数据校验
    l1=len(Dfig_char)#属性不同取值个数
    l1p=len(Darr)#属性不同取值个数
    if l1!=l1p:
        print("error1:check the second and third parameters of function of comSD")
        exit()

    ks=len(Darr[0])#第1个属性取值的数据中标签（种类）个数
    nums=0#从Darr中计算的总样本中样例的数目
    Dv=[]#列表，存放不同属性取值的子样本中样例的数目
    for i in range(l1):#对不同属性取值循环
        #标签（种类）个数的数据校验
        if i !=0 :
           k=len(Darr[i])#除第1个属性取值的其他取值数据中标签（种类）个数
           if k != ks:
               print("error2:check the third parameter of function of comSD")
               exit()
        tempI=sum(Darr[i])#不同属性取值的子样本中样例的数目
        Dv.append(tempI)
        nums=nums+tempI
    if D > 0:
        #样本中样例数目的数据校验
        if nums!=D:
            print("error3:check the third and forth parameters of function of comSD")
            exit()
    if D <= 0:
        D=nums

    Splus=0#信息增益
    for i in range(l1):#对不同属性取值循环
#        print('i-value',i)
        Stemp=comS(Darr[i],0) #计算不同属性的信息熵
        if diaflag==2:
            print(floorchar + ':', Dfig_char[i], "信息量:", Stemp)
        Stempw=(Dv[i]/D)*Stemp   #信息熵的加权
        if diaflag>=1:
            print(floorchar+':',Dfig_char[i],"信息量加权:", Stempw)
        Splus=Splus+Stempw
    return Splus




#- 训练集格式化
#- 属性字符串
'''fnc=['色泽','根蒂','敲声','纹理','脐部','触感']
#- 标签字符串
tnc=['好','坏']
#- 属性取值字符串
fnvc1=['青绿','乌黑','浅白']
fnvc2=['蜷缩','稍蜷','硬挺']
fnvc3=['浊响','沉闷','清脆']
fnvc4=['清晰','稍糊','模糊']
fnvc5=['凹陷','稍凹','平坦']
fnvc6=['硬滑','软粘']
fnvc=[fnvc1,fnvc2,fnvc3,fnvc4,fnvc5,fnvc6]'''
#- 数据集
#- 属性取值按索引号数值化，注意此例是从1开始。如第一个属性对应色泽，数字3对应浅白
#- 标签类别按索引号数值化，注意此例是从0开始。
data=[[1,1,1,1,1,1,0],[2,1,2,1,1,1,0],[2,1,1,1,1,1,0],
      [1,1,2,1,1,1,0],[5,3,1,1,1,1,0],[1,2,1,1,2,2,0],
      [2,2,1,2,2,2,0],[2,2,1,1,2,1,0],[2,2,2,2,2,1,1],
      [1,3,3,1,3,2,1],[3,3,3,3,3,1,1],[3,1,1,3,3,2,1],
      [1,2,1,2,1,1,1],[3,2,2,2,1,1,1],[2,2,1,1,2,2,1],
      [3,1,1,3,3,1,1],[1,1,2,2,2,1,1]]
fign=len(fnc)#属性个数
datan=len(data)#数据集样例个数
kn=len(tnc)#类别个数
localflow='根结点'
Gaina=np.zeros(fign)#



def find_the_best_fnc(fnc,fnvc,data,datan,diaflag=0):#若diaflag=1,则打印细致过程

    tempchar0 = '=========='
    tempcharx = '**********'
    tempcharsp = '  '
    for i in range(fign): #扫描不同属性
        tempchar1='按'+fnc[i]+'划分'
        inforchar=tempchar0+tempchar1+tempchar0
        if diaflag==1 :
          print(inforchar)

        #构造每个属性的分类情况列表，以用函数comSD计算信息增益
        D1_X_arr=[]
        figvn=len(fnvc[i])#第i个属性的取值个数
        #每个取值的各个例子数目
        tempsub=np.zeros((figvn,kn),dtype=int)#某属性不同属性值的分类数据
        #print(tempsub)
        for j in range(datan):#扫描不同样例
            for k in range(figvn):#扫描不同属性值
                kp=k+1#数据中不同属性取值从1开始排序
                if data[j][i]==kp:
                    for l in range(kn):#扫描不同种类
    #                   if data[j][fign]==l:
                        if data[j][-1] == l:
                            tempsub[k][l]=tempsub[k][l]+1
        tempcsd=comSD(localflow, fnvc[i], tempsub, 0,1)

        Dsample = np.zeros(kn, dtype=int)
        # print(Dsample)
        for l in range(kn):
            for k in range(figvn):
                Dsample[l] = Dsample[l] + tempsub[k][l]
        S = comS(Dsample, 0)

        Gaina[i] = S - tempcsd
        if diaflag == 1:
            print(tempchar1, '划分后信息熵增益为：', Gaina[i])
    tempI=np.argmax(Gaina) #取信息增益最大值对应的序号
    optfig=fnc[tempI]
    tempchar=tempchar0*2+tempcharsp+tempcharx+tempcharsp+tempchar0*2
    print(tempchar)
    print('当前最优划分属性：',optfig)
    print('划分后信息熵增益为：', Gaina[tempI])
    print(tempchar)














