import numpy as np
import matplotlib.pyplot as plt


def gm11(x0, forecast=5):
    """
    GM(1,1) 模型预测函数

    参数:
        x0: 原始数据序列（list 或 1D numpy 数组）
        forecast: 预测步数 (例如预测未来 forecast 个时间点)

    返回:
        x0_pred: 原始数据拟合及预测值（包含已有数据点与预测点）
        a, b: 模型参数
    """
    x0 = np.array(x0).astype(float)
    n = x0.shape[0]

    # 1. 累加生成 (AGO)
    x1 = np.cumsum(x0)

    # 2. 构造背景值序列 z，其中 z(k) = 0.5 * (x1(k)+x1(k-1))
    z = np.array([0.5 * (x1[k] + x1[k - 1]) for k in range(1, n)])

    # 3. 建立矩阵 B 和向量 Y
    B = np.column_stack((-z, np.ones(n - 1)))
    Y = x0[1:].reshape((n - 1, 1))

    # 4. 利用最小二乘法求解参数 [a, b]^T
    params = np.linalg.lstsq(B, Y, rcond=None)[0].flatten()
    a, b = params[0], params[1]

    # 5. 根据模型求解累计预测值
    def x1_hat(k):
        return (x0[0] - b / a) * np.exp(-a * (k - 1)) + b / a

    # 生成预测值，从 1 到 n+forecast 的 x1 值
    x1_pred = np.array([x1_hat(k) for k in range(1, n + forecast + 1)])

    # 6. 求原始序列预测值（一次差分）
    x0_pred = np.empty_like(x1_pred)
    x0_pred[0] = x0[0]  # 保持初始值一致
    x0_pred[1:] = x1_pred[1:] - x1_pred[:-1]

    return x0_pred, a, b


def posterior_ratio(actual, predicted):
    """
    计算后验差值比: 残差标准差与原始数据标准差的比值
    参数:
        actual: 实际数据 (训练部分)
        predicted: 预测数据 (训练部分)
    返回:
        C: 后验差值比
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    residuals = actual - predicted
    return np.std(residuals) / np.std(actual)


# 示例数据：2013 到 2023 共11年的城市人口数据（单位：万人）
urban_population = [74502, 76738, 79302, 81924, 84343, 86433, 88426,
                    90220, 91425, 92071, 93267]
# 农村数据
rural_population = [62224, 60908, 59024, 57308, 55668, 54108, 52582,
                    50992, 49835, 49104, 47700]

forecast_years = 5  # 预测未来 5 年

# 城市人口预测
urban_pred, a_urban, b_urban = gm11(urban_population, forecast=forecast_years)
# 农村人口预测
rural_pred, a_rural, b_rural = gm11(rural_population, forecast=forecast_years)

# 计算后验差值比（只计算训练期部分数据对比）
n = len(urban_population)
urban_C = posterior_ratio(urban_population, urban_pred[:n])
rural_C = posterior_ratio(rural_population, rural_pred[:n])

# 构造年份标签，包括历史数据和预测数据
years = list(range(2013, 2013 + len(urban_pred)))

# 绘图
plt.figure(figsize=(12, 6))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制城市人口数据与预测值
plt.subplot(1, 2, 1)
plt.plot(years, urban_pred, 'r--o', label="预测")
plt.plot(range(2013, 2013 + n), urban_population, 'bo-', label="实际")
plt.title("城市人口预测")
plt.xlabel("年份")
plt.ylabel("人口数量（单位：万）")
plt.legend()
# 在图中添加后验差值比
plt.text(0.5, 0.1, f"后验差值比: {urban_C:.3f}",
         transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

# 绘制农村人口数据与预测值
plt.subplot(1, 2, 2)
plt.plot(years, rural_pred, 'r--o', label="预测")
plt.plot(range(2013, 2013 + n), rural_population, 'bo-', label="实际")
plt.title("农村人口预测")
plt.xlabel("年份")
plt.ylabel("人口数量（单位：万）")
plt.legend()
# 在图中添加后验差值比
plt.text(0.5, 0.1, f"后验差值比: {rural_C:.3f}",
         transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

plt.tight_layout()
plt.show()

# 输出模型参数和后验差值比
print("城市人口模型参数: a = {:.4f}, b = {:.4f}".format(a_urban, b_urban))
print("城市人口预测值:", urban_pred)
print("城市人口后验差值比: {:.3f}".format(urban_C))
print("农村人口模型参数: a = {:.4f}, b = {:.4f}".format(a_rural, b_rural))
print("农村人口预测值:", rural_pred)
print("农村人口后验差值比: {:.3f}".format(rural_C))
