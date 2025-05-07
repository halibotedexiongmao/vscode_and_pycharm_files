# ---------------------- 数据定义部分 ----------------------

# 属性名称列表 (对应数据集中的六个特征)
# 索引顺序：[色泽, 根蒂, 敲声, 纹理, 脐部, 触感]
fnc = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感']

# 类别标签列表 (0: 坏瓜，1: 好瓜)
tnc = ['坏瓜', '好瓜']

# 特征取值列表 (每个特征的候选值集合)
# 结构说明：
# [
#    ['青绿', '乌黑', '浅白'],       # 色泽 (索引0)
#    ['蜷缩', '稍蜷', '硬挺'],       # 根蒂 (索引1)
#    ['浊响', '沉闷', '清脆'],       # 敲声 (索引2)
#    ['清晰', '稍糊', '模糊'],       # 纹理 (索引3)
#    ['凹陷', '稍凹', '平坦'],       # 脐部 (索引4)
#    ['硬滑', '软粘']               # 触感 (索引5，只有两个取值)
# ]
fnvc = [
    ['青绿', '乌黑', '浅白'],
    ['蜷缩', '稍蜷', '硬挺'],
    ['浊响', '沉闷', '清脆'],
    ['清晰', '稍糊', '模糊'],
    ['凹陷', '稍凹', '平坦'],
    ['硬滑', '软粘']
]

# 修正后的数据集
# 数据结构说明：
# 每个样本格式：[色泽取值, 根蒂取值, 敲声取值, 纹理取值, 脐部取值, 触感取值, 类别标签]
# 特征取值说明：
#   数值为1-based索引（例如色泽取值1对应"青绿"，2对应"乌黑"，3对应"浅白"）
# 类别标签说明：
#   0表示坏瓜，1表示好瓜
data = [
    [1, 1, 1, 1, 1, 1, 1], [2, 1, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 1, 1, 1, 1], [3, 1, 1, 1, 1, 1, 1], [1, 2, 1, 1, 2, 2, 1],
    [2, 2, 1, 2, 2, 2, 1], [2, 2, 1, 1, 2, 1, 1], [2, 2, 2, 2, 2, 1, 0],
    [1, 3, 3, 1, 3, 2, 0], [3, 3, 3, 3, 3, 1, 0], [3, 1, 1, 3, 3, 2, 0],
    [1, 2, 1, 2, 1, 1, 0], [3, 2, 2, 2, 1, 1, 0], [2, 2, 1, 1, 2, 2, 0],
    [3, 1, 1, 3, 3, 1, 0], [1, 1, 2, 2, 2, 1, 0]
]


# ---------------------- 核心函数部分 ----------------------

def comS(karr):
    """
    计算信息熵
    参数：
        karr : 类别计数数组 (例如：[坏瓜数量, 好瓜数量])
    返回：
        信息熵值 (单位：比特)
    """
    total = sum(karr)
    if total == 0: return 0  # 处理空数据情况
    entropy = 0.0
    for k in karr:
        if k == 0: continue  # 0值项对熵无贡献
        p = k / total
        entropy -= p * math.log2(p)
    return entropy


def calculate_information_gain(data, feature_idx):
    """
    计算指定特征的信息增益
    参数：
        data : 当前数据集
        feature_idx : 特征索引 (0-based，对应fnc列表的索引)
    返回：
        该特征的信息增益值
    """
    # 获取该特征可能的取值数量
    feat_values = len(fnvc[feature_idx])

    # 初始化分类统计矩阵 [特征取值][类别]
    class_counts = [[0] * len(tnc) for _ in range(feat_values)]

    # 遍历所有样本进行统计
    for sample in data:
        val = sample[feature_idx] - 1  # 将1-based转换为0-based索引
        label = sample[-1]
        class_counts[val][label] += 1

    # 计算总体熵
    total_counts = [sum(c) for c in zip(*class_counts)]  # 转置求和得到类别总数
    total_entropy = comS(total_counts)

    # 计算条件熵
    cond_entropy = 0.0
    total_samples = len(data)
    for counts in class_counts:
        subset_sum = sum(counts)
        if subset_sum == 0: continue  # 跳过空子集
        cond_entropy += (subset_sum / total_samples) * comS(counts)

    return total_entropy - cond_entropy  # 信息增益 = 总熵 - 条件熵


def get_majority_class(data):
    """
    获取多数类别（用于处理无法划分的情况）
    参数：
        data : 当前数据集
    返回：
        多数类别的标签 (0或1)
    """
    counts = {}
    for sample in data:
        label = sample[-1]
        counts[label] = counts.get(label, 0) + 1
    return max(counts, key=lambda k: counts[k])


def build_tree(data, features, parent_majority=None):
    """
    递归构建决策树
    参数：
        data : 当前数据集
        features : 可用特征索引列表
        parent_majority : 父节点的多数类（用于处理空分支）
    返回：
        决策树节点 (字典结构)
    """
    # 处理空数据集情况
    if not data:
        return {'class': parent_majority}

    # 获取当前数据多数类
    current_majority = get_majority_class(data)

    # 终止条件1: 所有样本同一类
    if len(set(s[-1] for s in data)) == 1:
        return {'class': data[0][-1]}

    # 终止条件2: 无剩余特征
    if not features:
        return {'class': current_majority}

    # 选择最佳划分特征
    best_gain = -1
    best_feat = None
    for feat in features:
        gain = calculate_information_gain(data, feat)
        if gain > best_gain:
            best_gain = gain
            best_feat = feat

    # 创建结点
    node = {
        'feature': fnc[best_feat],  # 特征名称
        'children': {}  # 子节点字典
    }

    # 递归构建子树
    remaining_features = [f for f in features if f != best_feat]
    for value in fnvc[best_feat]:
        value_idx = fnvc[best_feat].index(value) + 1  # 获取1-based索引
        subset = [s for s in data if s[best_feat] == value_idx]
        node['children'][value] = build_tree(
            subset,
            remaining_features,
            current_majority  # 传递当前多数类用于处理空分支
        )

    return node


# ---------------------- 执行构建 ----------------------

import json
import math
import numpy as np

# 初始化所有可用特征索引 (0-based)
all_features = list(range(len(fnc)))
# 构建决策树
decision_tree = build_tree(data, all_features)

# ---------------------- 结果展示 ----------------------

print(json.dumps(decision_tree, indent=2, ensure_ascii=False))