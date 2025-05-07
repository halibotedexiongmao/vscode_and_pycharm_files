'''def a():
    print('hello')

def b(x):
    print('haha')
    x()
    print('hehe')

import numpy as np

# 定义三个维度的大小
d0 = 4  # 第一个维度的大小
d1 = 3  # 第二个维度的大小
d2 = 2  # 第三个维度的大小

# 生成一个形状为 (d0, d1, d2) 的三维数组
three_dimensional_array = np.random.randn(d0, d1, d2,2)

print(three_dimensional_array)
'''
import numpy as np
w_true = np.array([1.5, -2.0])
b_true = 0.5

# 计算线性组合并通过sigmoid函数生成概率
z = X.dot(w_true) + b