import numpy as np

# 1. 随机生成样本数据
np.random.seed(42)  # 设置随机种子保证可重复性
n_samples = 1000
n_features = 2

# 生成特征矩阵（标准正态分布）
X = np.random.randn(n_samples, n_features)
# 设置真实模型参数
w_true = np.array([1.5, -2.0])
b_true = 0.5

# 计算线性组合并通过sigmoid函数生成概率
z = X.dot(w_true) + b_true
p = 1 / (1 + np.exp(-z))


# 根据概率生成二分类标签
y = (np.random.rand(n_samples) < p).astype(int)


# 2. 实现逻辑斯蒂回归模型
class LogisticRegression:
    def __init__(self, learning_rate=0.1, max_iter=1000, tol=1e-4):
        self.learning_rate = learning_rate  # 学习率
        self.max_iter = max_iter  # 最大迭代次数
        self.tol = tol  # 收敛阈值
        self.w = None  # 权重系数
        self.b = None  # 偏置项

    def sigmoid(self, z):
        """Sigmoid激活函数"""
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        """训练模型"""
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)  # 初始化权重
        self.b = 0.0  # 初始化偏置

        # 梯度下降优化
        for i in range(self.max_iter):
            # 计算预测值
            linear_model = np.dot(X, self.w) + self.b
            y_pred = self.sigmoid(linear_model)

            # 计算梯度
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            # 记录旧参数用于收敛判断
            prev_w = self.w.copy()
            prev_b = self.b

            # 参数更新
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db

            # 收敛检查（参数变化小于阈值时停止）
            if np.linalg.norm(self.w - prev_w) < self.tol and abs(self.b - prev_b) < self.tol:
                print(f"训练提前收敛于第{i}次迭代")
                break

    def predict_prob(self, X):
        """返回预测概率"""
        linear_model = np.dot(X, self.w) + self.b
        return self.sigmoid(linear_model)

    def predict(self, X, threshold=0.5):
        """返回类别预测结果"""
        prob = self.predict_prob(X)
        return (prob >= threshold).astype(int)


# 实例化并训练模型
model = LogisticRegression(learning_rate=0.1, max_iter=1000)
model.fit(X, y)

# 输出训练结果
print("真实权重：", w_true)
print("训练得到权重：", model.w)
print("\n真实偏置：", b_true)
print("训练得到偏置：", model.b)

# 计算准确率
y_pred = model.predict(X)
accuracy = np.mean(y == y_pred)
print("\n训练集准确率：", accuracy)
