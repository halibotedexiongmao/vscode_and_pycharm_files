import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义函数，处理分母为0的情况
def f(x, y):
    with np.errstate(divide='ignore', invalid='ignore'):
        z = (x * y) / (x**2 + y**2)
        z = np.where((x == 0) & (y == 0), np.nan, z)
    return z

# 创建网格
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# 绘制三维曲面图
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D Plot of f(x, y) = xy/(x² + y²)')
plt.show()

# 沿不同路径y = kx的函数值
x_line = np.linspace(-1, 1, 100)
k_values = [0, 0.5, 1, 2]

plt.figure(figsize=(10, 6))
for k in k_values:
    if k == 0:
        y_line = np.zeros_like(x_line)  # y=0
    else:
        y_line = k * x_line  # y = kx
    z_line = f(x_line, y_line)
    plt.plot(x_line, z_line, label=f'y = {k}x')

plt.xlabel('x')
plt.ylabel('f(x, y)')
plt.title('Function Values Along Paths y = kx')
plt.legend()
plt.grid(True)
plt.show()

# 固定x，y趋近于0时的函数行为
y_values = np.linspace(-0.1, 0.1, 100)
x_fixed = 0.1
z_fixed_x = f(x_fixed * np.ones_like(y_values), y_values)

plt.figure(figsize=(10, 6))
plt.plot(y_values, z_fixed_x)
plt.xlabel('y')
plt.ylabel('f(x=0.1, y)')
plt.title('Behavior as y → 0 with Fixed x=0.1')
plt.grid(True)
plt.show()

# 固定y，x趋近于0时的函数行为
x_values = np.linspace(-0.1, 0.1, 100)
y_fixed = 0.1
z_fixed_y = f(x_values, y_fixed * np.ones_like(x_values))

plt.figure(figsize=(10, 6))
plt.plot(x_values, z_fixed_y)
plt.xlabel('x')
plt.ylabel('f(x, y=0.1)')
plt.title('Behavior as x → 0 with Fixed y=0.1')
plt.grid(True)
plt.show()