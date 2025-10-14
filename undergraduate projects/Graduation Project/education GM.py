import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def gm11(x0, predict_step=3):
    """
    使用 GM(1,1) 模型对单个序列进行拟合和预测

    参数：
    -----------
    x0 : list 或 ndarray
        原始序列 (x^(0))
    predict_step : int
        向后预测的步数

    返回：
    -----------
    x0_hat : ndarray
        对原始序列的拟合值（含起始值）
    forecast : ndarray
        向后预测的 predict_step 步预测值
    a, b : float
        GM(1,1) 模型参数
    """
    x0 = np.array(x0, dtype=float)
    n = len(x0)
    # 1. 累加生成 (AGO)
    x1 = np.cumsum(x0)

    # 2. 构造背景值序列 z1
    z1 = (x1[:-1] + x1[1:]) / 2.0  # 长度 n-1
    # 构造矩阵 B 和向量 Y，注意 GM(1,1) 模型的离散化表达式为：x0(k+1) + a*z1(k)=b
    B = np.column_stack([-z1, np.ones(n - 1)])
    Y = x0[1:].reshape(-1, 1)

    # 3. 使用最小二乘法估计参数 [a, b]
    AB = np.linalg.inv(B.T @ B) @ B.T @ Y
    a, b = AB[0, 0], AB[1, 0]

    # 4. 构造 x1 的预测模型
    def x1_hat(k):
        return (x1[0] - b / a) * np.exp(-a * (k - 1)) + b / a

    # 5. 利用逆累加生成得到 x0 的拟合序列
    x0_hat = [x0[0]]  # 初始值相同
    for k in range(2, n + 1):
        x0_hat.append(x1_hat(k) - x1_hat(k - 1))
    x0_hat = np.array(x0_hat)

    # 6. 预测未来 predict_step 步
    forecast = []
    for i in range(1, predict_step + 1):
        forecast_val = x1_hat(n + i) - x1_hat(n + i - 1)
        forecast.append(forecast_val)
    forecast = np.array(forecast)

    return x0_hat, forecast, a, b


def calc_posterior_error_ratio(x0, x0_hat):
    """
    计算后验差值比，即残差的标准差与原始数据标准差的比值。

    参数：
    -----------
    x0 : ndarray
        原始数据序列
    x0_hat : ndarray
        拟合数据序列（与 x0 长度相同）

    返回：
    -----------
    ratio : float
        后验差值比
    """
    residual = x0 - x0_hat
    std_res = np.std(residual, ddof=1)
    std_orig = np.std(x0, ddof=1)
    ratio = std_res / std_orig if std_orig != 0 else np.nan
    return ratio


# ===============================
# 模拟数据：请用实际数据替换以下数值
# 设定时间范围 2013-2023（11年）
# 原始年份
years = np.array([2013, 2014, 2016, 2017, 2018, 2019, 2021, 2022, 2023])  # 去掉了2015和2020

# 对应地，data_dict 里每个数据列表也去掉2015年的值（位置应对）

# 定义多个类别的数据，每个类别均为 11 个数据
data_dict = {
    "6岁及6岁以上未上过学人口数": [52010, 56255, 61448, 56152, 57483, 51892, 51186, 51393, 55292],
    "6岁及6岁以上小学人口数": [274658, 274858, 275939, 268406, 268951,
                     257030, 365918, 355354, 350424],
    "6岁及6岁以上初中人口数": [425144, 420432, 418395, 404872, 401864,
                     379039, 487144, 467993, 511117],
    "6岁及6岁以上高中人口数": [172088, 174847, 182171, 186735, 186794,
                     180285, 233626, 222881, 221678],
    "6岁及6岁以上大专及以上人口数": [117925, 120698, 139370, 147593, 149104,
                        148170, 264467, 265414, 270529],
}

# 预测未来步数，例如预测未来 3 年（2024-2026）
predict_step = 5
future_years = np.arange(years[-1] + 1, years[-1] + 1 + predict_step)

# 用于存储结果
results = {}

# 对每个序列进行 GM(1,1) 拟合与预测，并计算后验差值比
for category, data in data_dict.items():
    data = np.array(data, dtype=float)
    fitted, forecast, a, b = gm11(data, predict_step=predict_step)
    posterior_ratio = calc_posterior_error_ratio(data, fitted)
    results[category] = {
        "data": data,
        "fitted": fitted,
        "forecast": forecast,
        "a": a,
        "b": b,
        "posterior_ratio": posterior_ratio
    }

# ===============================
# 绘图：将历史数据、拟合数据与预测数据绘制在同一图中，并标注后验差值比

plt.figure(figsize=(12, 8))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
color_list = ['b', 'g', 'r', 'c', 'm', 'orange']
for i, (category, res) in enumerate(results.items()):
    # 拼接年份：历史年份和未来年份
    all_years = np.concatenate([years, future_years])
    # 拼接数据：拟合数据与预测数据（预测部分以虚线显示）
    fitted_full = np.concatenate([res["fitted"], res["forecast"]])

    # 绘制历史数据（散点）和拟合预测曲线
    plt.plot(years, res["data"], 'o', color=color_list[i], label=f"{category} 实际")
    plt.plot(all_years, fitted_full, '-', color=color_list[i],
             label=f"{category} 拟合/预测 (后验比={res['posterior_ratio']:.3f})")

plt.xlabel("年份")
plt.ylabel("人口数（人）")
plt.title("不同受教育程度人口数预测结果\nGM(1,1) 模型")
plt.grid(True)

# 将图例放到图外右侧
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()
