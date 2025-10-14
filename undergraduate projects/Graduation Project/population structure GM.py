import numpy as np
import matplotlib.pyplot as plt


class GM11:
    def __init__(self, data, predict_step=5):
        self.data = np.array(data, dtype=np.float64)
        self.predict_step = predict_step
        self.a = None
        self.b = None
        self.C = None
        self.mape = 0.0
        self.fitted_values = np.zeros_like(self.data)
        self.valid = True

    def _ratio_test(self):
        ratios = self.data[:-1] / self.data[1:]
        lower = np.exp(-2 / (len(self.data) + 1))
        upper = np.exp(2 / (len(self.data) + 1))
        return np.all((ratios > lower) & (ratios < upper))

    def fit(self):
        if not self._ratio_test():
            self.valid = False
            self.fitted_values = self.data.copy()
            return

        AGO = np.cumsum(self.data).reshape(-1, 1)
        B = np.ones((len(self.data) - 1, 2))
        B[:, 0] = -0.5 * (AGO[:-1] + AGO[1:]).flatten()
        Y = self.data[1:].reshape(-1, 1)

        try:
            [[a], [b]] = np.linalg.inv(B.T @ B) @ B.T @ Y
        except np.linalg.LinAlgError:
            a, b = 0.1, 0.1  # 处理奇异矩阵

        self.a, self.b = a, b
        self.fitted_values = (self.data[0] - b / a) * (1 - np.exp(a)) * np.exp(-a * np.arange(len(self.data)))

        residuals = self.data - self.fitted_values
        S1 = np.var(self.data, ddof=1)
        S2 = np.var(residuals, ddof=1)
        self.C = S2 / S1
        self.mape = np.mean(np.abs((self.data - self.fitted_values) / self.data)) * 100

    def predict(self):
        t = np.arange(len(self.data), len(self.data) + self.predict_step)
        return (self.data[0] - self.b / self.a) * (1 - np.exp(self.a)) * np.exp(-self.a * t)


# 数据准备
data = {
    "0-14": [22423, 22712, 22824, 23252, 23522, 23751, 23689, 25277, 24678, 23908, 23063],
    "15-64": [101041, 101032, 100978, 100943, 100528, 100065, 99552, 96871, 96526, 96289, 96228],
    "65+": [13262, 13902, 14524, 15037, 15961, 16724, 17767, 19064, 20056, 20978, 21676]
}

# 时间轴设置
years = np.arange(2013, 2024)
forecast_steps = 5
all_years = np.append(years, years[-1] + np.arange(1, forecast_steps + 1))

plt.figure(figsize=(12, 8))
colors = {'0-14': '#1f77b4', '15-64': '#ff7f0e', '65+': '#2ca02c'}
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

for age_group, series in data.items():
    # 正确初始化模型
    model = GM11(np.array(series), forecast_steps)
    model.fit()  # 必须先拟合

    # 获取预测结果
    forecast = np.concatenate([model.fitted_values, model.predict()])

    # 绘制实际数据点
    plt.scatter(years, series, color=colors[age_group],
                edgecolor='k', zorder=5, label=f'{age_group}实际')

    # 绘制预测曲线
    plt.plot(all_years, forecast, '--', color=colors[age_group],
             label=f'{age_group}预测\n(C={model.C:.4f})')

plt.axvline(2023.5, color='gray', linestyle=':', alpha=0.8)
plt.title("不同年龄段人口GM(1,1)预测 (2013-2028)", fontsize=14)
plt.xlabel("年份")
plt.ylabel("人口数量（万人）")
plt.xticks(all_years[::2], rotation=45)
plt.grid(linestyle='--', alpha=0.6)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()