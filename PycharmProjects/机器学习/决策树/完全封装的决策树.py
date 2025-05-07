import math
import json


def build_decision_tree(data):
    """
    构建决策树主函数
    参数：
        data : 字典列表格式的数据集，每个字典表示一个样本
               格式要求：{"特征1": 值, ..., "label": 类别标签}
    返回：
        决策树结构的嵌套字典
    """

    # ================== 数据预处理阶段 ==================
    # 初始化元数据存储字典
    metadata = {
        'attributes': [key for key in data[0] if key != 'label'],  # 提取特征名称列表（排除label）
        'attribute_values': {},  # 存储每个特征的取值范围 {特征名: [值1, 值2...]}
        'class_labels': set()  # 存储所有类别标签
    }

    # 遍历数据集收集元数据
    for sample in data:
        # 收集类别标签
        metadata['class_labels'].add(sample['label'])

        # 收集每个特征的取值范围
        for attr in metadata['attributes']:
            # 如果特征尚未记录，初始化空集合
            if attr not in metadata['attribute_values']:
                metadata['attribute_values'][attr] = set()
            # 添加当前样本的特征值
            metadata['attribute_values'][attr].add(sample[attr])
            print(metadata)

    # 转换格式：集合转排序列表（保证顺序一致性）
    for attr in metadata['attribute_values']:
        metadata['attribute_values'][attr] = sorted(metadata['attribute_values'][attr])
    metadata['class_labels'] = sorted(metadata['class_labels'])

    # ================== 核心功能函数定义 ==================
    def calculate_entropy(class_counts):
        """
        计算信息熵
        参数：
            class_counts : 类别计数列表，例如[5,3]表示两个类各有5个和3个样本
        返回：
            信息熵值（单位：比特）
        """
        total = sum(class_counts)
        if total == 0:
            return 0  # 处理空数据情况
        entropy = 0.0
        for count in class_counts:
            if count == 0:
                continue  # 0值项不参与计算
            probability = count / total
            entropy -= probability * math.log2(probability)
        return entropy

    def information_gain(subset_data, attribute):
        """
        计算指定特征的信息增益
        参数：
            subset_data : 当前数据子集
            attribute   : 要计算的特征名
        返回：
            该特征的信息增益值
        """
        # 初始化值分布字典
        value_distribution = {}
        # 创建类别索引映射（用于列表定位）
        class_index = {label: i for i, label in enumerate(metadata['class_labels'])}

        # 预先初始化所有可能取值的计数列表
        for value in metadata['attribute_values'][attribute]:
            value_distribution[value] = [0] * len(metadata['class_labels'])

        # 统计每个值下的类别分布
        for sample in subset_data:
            value = sample[attribute]
            label_idx = class_index[sample['label']]
            value_distribution[value][label_idx] += 1

        # 计算总熵
        total_counts = [
            sum(col) for col in zip(*value_distribution.values())
        ]
        total_entropy = calculate_entropy(total_counts)

        # 计算条件熵
        cond_entropy = 0.0
        total_samples = len(subset_data)
        for counts in value_distribution.values():
            subset_sum = sum(counts)
            if subset_sum == 0:
                continue  # 跳过空子集
            cond_entropy += (subset_sum / total_samples) * calculate_entropy(counts)

        return total_entropy - cond_entropy  # 信息增益 = 总熵 - 条件熵

    def majority_class(subset_data):
        """
        获取多数类别
        参数：
            subset_data : 当前数据子集
        返回：
            出现次数最多的类别标签
        """
        counter = {}
        for sample in subset_data:
            label = sample['label']
            # 使用get方法处理不存在的键
            counter[label] = counter.get(label, 0) + 1
        return max(counter, key=lambda k: counter[k])

    def tree_growth(subset_data, used_attributes, parent_majority):
        """
        递归构建决策树核心函数
        参数：
            subset_data      : 当前处理的数据子集
            used_attributes  : 已使用的特征集合
            parent_majority  : 父节点的多数类（用于处理空分支）
        返回：
            当前子树结构的字典
        """
        # 终止条件1：空数据集（使用父节点多数类）
        if not subset_data:
            return {'class': parent_majority}

        # 终止条件2：所有样本同类（返回叶节点）
        class_labels = set(s['label'] for s in subset_data)
        if len(class_labels) == 1:
            return {'class': subset_data[0]['label']}

        # 终止条件3：无可用特征（返回当前多数类）
        available_attributes = [
            a for a in metadata['attributes']
            if a not in used_attributes
        ]
        if not available_attributes:
            return {'class': majority_class(subset_data)}

        # 特征选择：寻找信息增益最大的特征
        best_gain = -1
        best_attr = None
        for attr in available_attributes:
            current_gain = information_gain(subset_data, attr)
            if current_gain > best_gain:
                best_gain = current_gain
                best_attr = attr

        # 创建决策节点
        node = {
            'attribute': best_attr,
            'children': {}
        }
        new_used = used_attributes.copy()
        new_used.add(best_attr)

        # 递归构建子树
        current_majority = majority_class(subset_data)
        for value in metadata['attribute_values'][best_attr]:
            # 筛选当前特征值的子集
            child_subset = [
                s for s in subset_data
                if s[best_attr] == value
            ]
            # 递归调用构建子树
            node['children'][value] = tree_growth(
                child_subset,
                new_used,
                current_majority
            )

        return node

    # ================== 执行决策树构建 ==================
    # 初始化多数类（处理空数据集情况）
    initial_majority = majority_class(data) if data else None
    # 启动递归构建过程
    return tree_growth(data, set(), initial_majority)


# ================== 使用示例 ==================
if __name__ == "__main__":
    # 测试数据集（同之前的西瓜数据集）

    # 完整的西瓜数据集示例
    watermelon_data = [
        {"色泽": "青绿", "根蒂": "蜷缩", "敲声": "浊响", "纹理": "清晰", "脐部": "凹陷", "触感": "硬滑",
         "label": "好瓜"},
        {"色泽": "乌黑", "根蒂": "蜷缩", "敲声": "沉闷", "纹理": "清晰", "脐部": "凹陷", "触感": "硬滑",
         "label": "好瓜"},
        {"色泽": "乌黑", "根蒂": "蜷缩", "敲声": "浊响", "纹理": "清晰", "脐部": "凹陷", "触感": "硬滑",
         "label": "好瓜"},
        {"色泽": "青绿", "根蒂": "蜷缩", "敲声": "沉闷", "纹理": "清晰", "脐部": "凹陷", "触感": "硬滑",
         "label": "好瓜"},
        {"色泽": "浅白", "根蒂": "蜷缩", "敲声": "浊响", "纹理": "清晰", "脐部": "凹陷", "触感": "硬滑",
         "label": "好瓜"},
        {"色泽": "青绿", "根蒂": "稍蜷", "敲声": "浊响", "纹理": "清晰", "脐部": "稍凹", "触感": "软粘",
         "label": "好瓜"},
        {"色泽": "乌黑", "根蒂": "稍蜷", "敲声": "浊响", "纹理": "稍糊", "脐部": "稍凹", "触感": "软粘",
         "label": "坏瓜"},
        {"色泽": "乌黑", "根蒂": "稍蜷", "敲声": "浊响", "纹理": "清晰", "脐部": "稍凹", "触感": "硬滑",
         "label": "好瓜"},
        {"色泽": "乌黑", "根蒂": "稍蜷", "敲声": "沉闷", "纹理": "稍糊", "脐部": "稍凹", "触感": "硬滑",
         "label": "坏瓜"},
        {"色泽": "青绿", "根蒂": "硬挺", "敲声": "清脆", "纹理": "清晰", "脐部": "平坦", "触感": "软粘",
         "label": "坏瓜"},
        {"色泽": "浅白", "根蒂": "硬挺", "敲声": "清脆", "纹理": "模糊", "脐部": "平坦", "触感": "硬滑",
         "label": "坏瓜"},
        {"色泽": "浅白", "根蒂": "蜷缩", "敲声": "浊响", "纹理": "模糊", "脐部": "平坦", "触感": "软粘",
         "label": "坏瓜"},
        {"色泽": "青绿", "根蒂": "稍蜷", "敲声": "浊响", "纹理": "稍糊", "脐部": "凹陷", "触感": "硬滑",
         "label": "坏瓜"},
        {"色泽": "浅白", "根蒂": "稍蜷", "敲声": "沉闷", "纹理": "稍糊", "脐部": "凹陷", "触感": "硬滑",
         "label": "坏瓜"},
        {"色泽": "乌黑", "根蒂": "稍蜷", "敲声": "浊响", "纹理": "清晰", "脐部": "稍凹", "触感": "软粘",
         "label": "坏瓜"},
        {"色泽": "浅白", "根蒂": "蜷缩", "敲声": "浊响", "纹理": "模糊", "脐部": "平坦", "触感": "硬滑",
         "label": "坏瓜"},
        {"色泽": "青绿", "根蒂": "蜷缩", "敲声": "沉闷", "纹理": "稍糊", "脐部": "稍凹", "触感": "硬滑",
         "label": "坏瓜"},
    ]

    # 构建决策树
    decision_tree = build_decision_tree(watermelon_data)

    # 打印决策树结构
    print(json.dumps(decision_tree, indent=2, ensure_ascii=False))


    # 定义预测函数
    def predict(tree, sample):
        """使用决策树进行分类预测"""
        if 'class' in tree:
            return tree['class']

        attr = tree['attribute']
        value = sample.get(attr, None)

        # 处理未知特征值
        if value not in tree['children']:
            return '未知类别'

        return predict(tree['children'][value], sample)


    # 测试样本预测
    test_sample = {
        "色泽": "青绿",
        "根蒂": "稍蜷",
        "敲声": "浊响",
        "纹理": "清晰",
        "脐部": "稍凹",
        "触感": "软粘"
    }
    print("预测结果:", predict(decision_tree, test_sample))