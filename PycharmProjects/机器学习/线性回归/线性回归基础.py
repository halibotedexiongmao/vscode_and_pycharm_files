import numpy as np

# 设置随机种子以保证可重复性
np.random.seed(0)

# 参数设置
n = 3  # 属性数量（不包括偏置）
N = 100  # 样本数量

# 生成样本数据
X = np.random.randn(n, N)  # 前n行是属性
X = np.vstack([X, np.ones(N)])  # 添加偏置项，形状变为(n+1)xN

# 生成真实权重（包括偏置项）
W_true = np.random.randn(n + 1, 1)

# 生成带噪声的标签
Y = W_true.T @ X + 0.1 * np.random.randn(1, N)

# 闭式解计算权重
XXT = X @ X.T
XXT_inv = np.linalg.inv(XXT)
W_closed = XXT_inv @ X @ Y.T

# 梯度下降法计算权重
learning_rate = 0.01
iterations = 1000
W_gd = np.zeros((n + 1, 1))  # 初始权重

for _ in range(iterations):
    error = Y - W_gd.T @ X
    gradient = X @ error.T  # 根据题目提示的梯度公式
    W_gd += learning_rate * gradient

# 输出结果
print("真实权重:\n", W_true)
print("闭式解权重:\n", W_closed)
print("梯度下降权重:\n", W_gd)

# 计算均方误差
mse_closed = np.mean((Y - W_closed.T @ X) ** 2)
mse_gd = np.mean((Y - W_gd.T @ X) ** 2)
print("\n闭式解均方误差:", mse_closed)
print("梯度下降均方误差:", mse_gd)