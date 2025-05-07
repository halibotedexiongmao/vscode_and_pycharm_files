


import numpy as np

# 1. 生成简单数据（2个特征，100个样本）
np.random.seed(0)  # 固定随机数
X = np.random.randn(100, 2)  # 特征矩阵
true_w = [2, -1]  # 真实权重
true_b = 0.3  # 真实偏置

# 生成标签（加入噪声）
scores = X[:, 0] * true_w[0] + X[:, 1] * true_w[1] + true_b
prob = 1 / (1 + np.exp(-scores))  # sigmoid转换概率
y = (prob > 0.5).astype(int)  # 二值化标签

# 2. 逻辑回归训练（极简版）
w = [0.0, 0.0]  # 初始化权重
b = 0.0  # 初始化偏置
lr = 0.1  # 学习率

# 训练100次
for _ in range(100):
    # 计算预测值
    z = X[:, 0] * w[0] + X[:, 1] * w[1] + b
    pred = 1 / (1 + np.exp(-z))

    # 计算梯度（手动计算）
    dw0 = np.mean((pred - y) * X[:, 0])  # 第一个特征的梯度
    dw1 = np.mean((pred - y) * X[:, 1])  # 第二个特征的梯度
    db = np.mean(pred - y)  # 偏置的梯度

    # 更新参数
    w[0] -= lr * dw0
    w[1] -= lr * dw1
    b -= lr * db

# 3. 结果展示
print("真实参数：", true_w, true_b)
print("训练结果：", [round(w[0], 2), round(w[1], 2)], round(b, 2))

# 计算准确率
pred_labels = (1 / (1 + np.exp(-(X[:, 0] * w[0] + X[:, 1] * w[1] + b)))) > 0.5
print("准确率:", np.mean(pred_labels == y))