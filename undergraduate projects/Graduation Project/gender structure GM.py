import numpy as np
import matplotlib.pyplot as plt


def gm11(x0, predict_len=5):
    """
    GM(1,1) 灰预测模型
    参数:
      x0: 原始数据序列（列表或一维 numpy 数组）
      predict_len: 需要预测的步长（默认预测未来5期）
    返回:
      x0_pred: 包含原始数据和预测数据的序列
      a, b: 模型参数
    """
    x0 = np.array(x0, dtype=float)
    n = len(x0)

    # 1. 累加生成序列：X(1)
    x1 = np.cumsum(x0)

    # 2. 计算背景值序列 Z(1)，常用取法为相邻两项的均值
    z1 = np.array([0.5 * (x1[i] + x1[i - 1]) for i in range(1, n)])

    # 3. 构造数据矩阵，利用最小二乘法估计参数 a 和 b
    B = np.column_stack((-z1, np.ones(n - 1)))
    Y = x0[1:].reshape((n - 1, 1))
    # 求解最小二乘问题，得到参数 a, b
    coeff, _, _, _ = np.linalg.lstsq(B, Y, rcond=None)
    a, b = coeff.flatten()

    # 4. 构造时间响应函数（X(1)的预测模型）
    def calc_x1(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a

    # 对累计序列进行预测
    x1_pred = np.array([calc_x1(k) for k in range(n + predict_len)])

    # 5. 差分还原得到原始序列 X(0) 的预测值
    x0_pred = np.empty(n + predict_len)
    x0_pred[0] = x0[0]
    for k in range(1, n + predict_len):
        x0_pred[k] = x1_pred[k] - x1_pred[k - 1]

    return x0_pred, a, b


# 示例数据（请用实际的男女人口数据替换下面的数据）
years = np.arange(2013, 2024)  # 2013-2023年
male_population = [70063, 70522, 70857, 71307, 71650, 71864, 72039,
                 72357, 72311, 72206, 72032]
female_population = [66663, 67124, 67469, 67925, 68361, 68677,
                   68969, 68855, 68949, 68969, 68935]

# 分别对男性和女性数据进行 GM(1,1) 预测，并预测未来5年
male_pred, male_a, male_b = gm11(male_population, predict_len=5)
female_pred, female_a, female_b = gm11(female_population, predict_len=5)

# 构造完整的年份数组（包括预测期）
years_pred = np.arange(2013, 2024 + 5)

# 计算后验差值比，只取历史数据部分
male_historical = np.array(male_population, dtype=float)
female_historical = np.array(female_population, dtype=float)
n_hist = len(male_historical)

male_residuals = male_historical - male_pred[:n_hist]
female_residuals = female_historical - female_pred[:n_hist]

male_posterior_ratio = np.std(male_residuals, ddof=1) / np.std(male_historical, ddof=1)
female_posterior_ratio = np.std(female_residuals, ddof=1) / np.std(female_historical, ddof=1)

# 输出后验差值比
print("男性后验差值比: {:.4f}".format(male_posterior_ratio))
print("女性后验差值比: {:.4f}".format(female_posterior_ratio))

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘图展示历史数据、预测数据以及后验差值比
plt.figure(figsize=(10, 6))
plt.plot(years, male_population, 'bo-', label="历史男性人口")
plt.plot(years_pred, male_pred, 'b--', label="预测男性人口")
plt.plot(years, female_population, 'ro-', label="历史女性人口")
plt.plot(years_pred, female_pred, 'r--', label="预测女性人口")

plt.xlabel("年份")
plt.ylabel("人口数")
plt.title("GM(1,1) 模型预测男女人口趋势及后验差值比")
plt.grid(True)
plt.legend()

# 在图中添加后验差值比信息
plt.text(0.2, 0.95, "男性后验差值比: {:.4f}".format(male_posterior_ratio),
         transform=plt.gca().transAxes, fontsize=12, color='blue',
         verticalalignment='top')
plt.text(0.2, 0.90, "女性后验差值比: {:.4f}".format(female_posterior_ratio),
         transform=plt.gca().transAxes, fontsize=12, color='red',
         verticalalignment='top')

plt.show()
